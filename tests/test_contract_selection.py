from datetime import date

from options_research.models import ContractSelectionRules, OptionQuote
from options_research.options import ContractSelector, implied_move_from_atm_straddle


def q(**overrides):
    values = {
        "ticker": "XYZ",
        "quote_date": date(2024, 2, 14),
        "expiry": date(2024, 3, 1),
        "option_type": "call",
        "strike": 105.0,
        "bid": 5.0,
        "ask": 5.5,
        "delta": 0.52,
        "volume": 500,
        "open_interest": 1200,
    }
    values.update(overrides)
    return OptionQuote(**values)


def test_option_quote_calculates_premium_volume_from_midpoint():
    quote = q(bid=1.0, ask=1.2, volume=250)

    assert quote.premium_volume == 27_500


def test_contract_selection_filters_by_min_premium_volume():
    rules = ContractSelectionRules(
        min_dte=5,
        max_dte=60,
        target_delta=0.55,
        delta_tolerance=0.12,
        max_spread_pct=0.20,
        min_volume=100,
        min_open_interest=250,
        min_premium_volume=50_000,
        prefer_expiry_after_event=True,
    )

    selected = ContractSelector(rules).select(
        quotes=[
            q(strike=105.0, bid=0.2, ask=0.22, volume=1_000, delta=0.55),
            q(strike=106.0, bid=2.4, ask=2.6, volume=250, delta=0.55),
        ],
        ticker="XYZ",
        quote_date=date(2024, 2, 14),
        underlying_price=100.0,
        event_date=date(2024, 2, 21),
    )

    assert selected is not None
    assert selected.strike == 106.0


def test_contract_selection_uses_premium_volume_as_liquidity_tiebreaker():
    rules = ContractSelectionRules(
        min_dte=5,
        max_dte=60,
        target_delta=0.55,
        delta_tolerance=0.12,
        max_spread_pct=0.20,
        min_volume=100,
        min_open_interest=250,
        prefer_expiry_after_event=True,
    )

    selected = ContractSelector(rules).select(
        quotes=[
            q(strike=105.0, bid=0.45, ask=0.55, volume=1_000, delta=0.55, open_interest=500),
            q(strike=106.0, bid=4.95, ask=5.05, volume=200, delta=0.55, open_interest=500),
        ],
        ticker="XYZ",
        quote_date=date(2024, 2, 14),
        underlying_price=100.0,
        event_date=date(2024, 2, 21),
    )

    assert selected is not None
    assert selected.strike == 106.0


def test_contract_selection_prefers_closest_expiry_after_earnings_with_liquidity_filters():
    rules = ContractSelectionRules(
        min_dte=5,
        max_dte=60,
        target_delta=0.55,
        delta_tolerance=0.12,
        max_spread_pct=0.20,
        min_volume=100,
        min_open_interest=250,
        prefer_expiry_after_event=True,
    )
    quotes = [
        q(expiry=date(2024, 2, 16), delta=0.55),  # before event, should lose to after-event expiry
        q(expiry=date(2024, 3, 15), delta=0.55),
        q(expiry=date(2024, 3, 1), delta=0.54),
        q(expiry=date(2024, 3, 1), delta=0.85),
        q(expiry=date(2024, 3, 1), bid=1.0, ask=1.8, delta=0.55),  # too wide
        q(expiry=date(2024, 3, 1), volume=10, delta=0.55),  # too illiquid
    ]

    selected = ContractSelector(rules).select(
        quotes=quotes,
        ticker="XYZ",
        quote_date=date(2024, 2, 14),
        underlying_price=100.0,
        event_date=date(2024, 2, 21),
    )

    assert selected is not None
    assert selected.expiry == date(2024, 3, 1)
    assert selected.delta == 0.54


def test_contract_selection_can_use_moneyness_when_delta_is_missing():
    rules = ContractSelectionRules(
        min_dte=10,
        max_dte=400,
        target_moneyness=1.05,
        moneyness_tolerance=0.04,
        min_volume=1,
        min_open_interest=1,
        max_spread_pct=0.50,
    )

    selected = ContractSelector(rules).select(
        quotes=[
            q(expiry=date(2025, 1, 17), strike=130.0, delta=None),
            q(expiry=date(2025, 1, 17), strike=106.0, delta=None),
        ],
        ticker="XYZ",
        quote_date=date(2024, 2, 14),
        underlying_price=100.0,
        event_date=None,
    )

    assert selected is not None
    assert selected.strike == 106.0


def test_implied_move_uses_atm_call_and_put_midpoints():
    call = q(option_type="call", strike=100.0, bid=4.8, ask=5.2)
    put = q(option_type="put", strike=100.0, bid=4.3, ask=4.7)

    assert implied_move_from_atm_straddle([call, put], underlying_price=100.0) == 0.095
