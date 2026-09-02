from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd

from .models import DataBundle, EarningsEvent, OptionQuote


EVENTS = {
    "NVDA": [date(2023, 2, 22), date(2023, 5, 24), date(2023, 8, 23), date(2024, 2, 21)],
    "TSLA": [date(2023, 1, 25), date(2023, 4, 19), date(2023, 10, 18), date(2024, 1, 24)],
    "ORCL": [date(2023, 3, 9), date(2023, 6, 12), date(2023, 9, 11), date(2024, 3, 11)],
    "AMD": [date(2023, 1, 31), date(2023, 5, 2), date(2023, 10, 31), date(2024, 1, 30)],
    "META": [date(2023, 2, 1), date(2023, 4, 26), date(2023, 10, 25), date(2024, 2, 1)],
}

BASE_PRICES = {"NVDA": 155.0, "TSLA": 125.0, "ORCL": 82.0, "AMD": 68.0, "META": 145.0}
EVENT_JUMPS = {"NVDA": 0.12, "TSLA": -0.07, "ORCL": 0.04, "AMD": 0.06, "META": 0.10}
DRIFT = {"NVDA": 0.0018, "TSLA": 0.0002, "ORCL": 0.0007, "AMD": 0.0011, "META": 0.0014}


def load_fixture_bundle() -> DataBundle:
    tickers = list(EVENTS)
    sessions = pd.bdate_range("2022-11-01", "2024-04-30").date
    prices = _make_prices(tickers, sessions)
    events = [
        EarningsEvent(ticker, event_date, "postmarket", event_date - timedelta(days=45))
        for ticker, dates in EVENTS.items()
        for event_date in dates
    ]
    options = _make_options(prices, events)
    return DataBundle(
        prices=prices,
        events=events,
        options=options,
        source="deterministic fixture data",
        notes=(
            "Synthetic but deterministic underlying and option-chain fixtures for "
            "NVDA, TSLA, ORCL, AMD, and META. Use for repeatable methodology tests; "
            "do not treat as market evidence."
        ),
    )


def _make_prices(tickers: Iterable[str], sessions: Iterable[date]) -> pd.DataFrame:
    rows = []
    session_list = list(sessions)
    for ticker in tickers:
        price = BASE_PRICES[ticker]
        event_lookup = {event_date: EVENT_JUMPS[ticker] for event_date in EVENTS[ticker]}
        for i, session in enumerate(session_list):
            deterministic_wave = 0.003 * np.sin(i / 9 + len(ticker))
            event_drift = _pre_earnings_drift(ticker, session)
            price *= 1 + deterministic_wave + DRIFT[ticker] + event_drift
            if _previous_session(session, session_list) in event_lookup:
                price *= 1 + event_lookup[_previous_session(session, session_list)]
            rows.append(
                {
                    "ticker": ticker,
                    "date": session,
                    "open": round(price * 0.997, 4),
                    "close": round(price, 4),
                }
            )
    return pd.DataFrame(rows)


def _pre_earnings_drift(ticker: str, session: date) -> float:
    for event_date in EVENTS[ticker]:
        days = (event_date - session).days
        if 1 <= days <= 30:
            return 0.0018 if ticker in {"NVDA", "META", "AMD"} else 0.0003
    return 0.0


def _previous_session(session: date, sessions: List[date]) -> date:
    idx = sessions.index(session)
    return sessions[max(0, idx - 1)]


def _make_options(prices: pd.DataFrame, events: List[EarningsEvent]) -> List[OptionQuote]:
    options: List[OptionQuote] = []
    price_lookup: Dict[tuple, float] = {
        (row.ticker, row.date): float(row.close) for row in prices.itertuples(index=False)
    }
    sessions_by_ticker = {
        ticker: sorted(prices.loc[prices["ticker"] == ticker, "date"].unique())
        for ticker in prices["ticker"].unique()
    }
    for event in events:
        sessions = sessions_by_ticker[event.ticker]
        event_idx = max(i for i, session in enumerate(sessions) if session <= event.event_date)
        base_idx = max(event_idx - 30, 0)
        base_underlying = price_lookup[(event.ticker, sessions[base_idx])]
        chain_strikes = [(round(base_underlying * mult, 2), delta) for mult, delta in [(1.00, 0.55), (1.05, 0.48), (1.15, 0.32)]]
        quote_offsets = [30, 20, 10, 5, 1, -1]
        for offset in quote_offsets:
            quote_idx = event_idx - offset
            if quote_idx < 0 or quote_idx >= len(sessions):
                continue
            quote_date = sessions[quote_idx]
            underlying = price_lookup[(event.ticker, quote_date)]
            expiry = _first_friday_after(event.event_date + timedelta(days=1))
            leaps_expiry = _third_friday_of_january(event.event_date.year + 1)
            for chosen_expiry in [expiry, leaps_expiry]:
                dte = max((chosen_expiry - quote_date).days, 1)
                for strike, delta in chain_strikes:
                    option_mid = _call_value(underlying, strike, dte, event.ticker, quote_date, event.event_date)
                    spread = max(0.10, option_mid * 0.08)
                    options.append(
                        OptionQuote(
                            ticker=event.ticker,
                            quote_date=quote_date,
                            expiry=chosen_expiry,
                            option_type="call",
                            strike=strike,
                            bid=round(max(option_mid - spread / 2, 0.01), 2),
                            ask=round(option_mid + spread / 2, 2),
                            delta=delta,
                            volume=250,
                            open_interest=1000,
                        )
                    )
                atm_strike = chain_strikes[0][0]
                put_mid = max(1.0, underlying * (0.055 + (dte / 365) * 0.08))
                spread = max(0.10, put_mid * 0.08)
                options.append(
                    OptionQuote(
                        ticker=event.ticker,
                        quote_date=quote_date,
                        expiry=chosen_expiry,
                        option_type="put",
                        strike=atm_strike,
                        bid=round(max(put_mid - spread / 2, 0.01), 2),
                        ask=round(put_mid + spread / 2, 2),
                        delta=-0.45,
                        volume=250,
                        open_interest=1000,
                    )
                )
    return options


def _call_value(
    underlying: float, strike: float, dte: int, ticker: str, quote_date: date, event_date: date
) -> float:
    intrinsic = max(underlying - strike, 0)
    time_value = underlying * (0.045 + (dte / 365) * 0.18)
    days_to_event = max((event_date - quote_date).days, 0)
    event_premium = underlying * max(0.0, 0.08 - days_to_event * 0.0015)
    ticker_tilt = underlying * (0.010 if ticker in {"NVDA", "META"} else 0.004)
    return max(0.35, intrinsic + time_value + event_premium + ticker_tilt)


def _first_friday_after(target: date) -> date:
    day = target
    while day.weekday() != 4:
        day += timedelta(days=1)
    return day


def _third_friday_of_january(year: int) -> date:
    day = date(year, 1, 1)
    fridays = []
    while day.month == 1:
        if day.weekday() == 4:
            fridays.append(day)
        day += timedelta(days=1)
    return fridays[2]
