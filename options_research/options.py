from __future__ import annotations

from datetime import date
from typing import Iterable, List, Optional

from .models import ContractSelectionRules, OptionQuote


class ContractSelector:
    def __init__(self, rules: ContractSelectionRules):
        self.rules = rules

    def select(
        self,
        quotes: Iterable[OptionQuote],
        ticker: str,
        quote_date: date,
        underlying_price: float,
        event_date: Optional[date],
    ) -> Optional[OptionQuote]:
        candidates = [
            quote
            for quote in quotes
            if quote.ticker == ticker
            and quote.quote_date == quote_date
            and quote.option_type.lower() == "call"
            and self._passes_base_filters(quote, quote_date)
            and self._passes_delta_or_moneyness(quote, underlying_price)
        ]
        if event_date and self.rules.prefer_expiry_after_event:
            after_event = [quote for quote in candidates if quote.expiry > event_date]
            candidates = after_event
        if not candidates:
            return None

        def rank(quote: OptionQuote) -> tuple:
            expiry_rank = abs((quote.expiry - event_date).days) if event_date else -self._dte(quote, quote_date)
            target_rank = self._target_distance(quote, underlying_price)
            return (expiry_rank, target_rank, quote.spread_pct, -quote.open_interest, -quote.volume)

        return sorted(candidates, key=rank)[0]

    def _passes_base_filters(self, quote: OptionQuote, quote_date: date) -> bool:
        dte = self._dte(quote, quote_date)
        return (
            self.rules.min_dte <= dte <= self.rules.max_dte
            and quote.bid >= 0
            and quote.ask > 0
            and quote.ask >= quote.bid
            and quote.spread_pct <= self.rules.max_spread_pct
            and quote.volume >= self.rules.min_volume
            and quote.open_interest >= self.rules.min_open_interest
        )

    def _passes_delta_or_moneyness(self, quote: OptionQuote, underlying_price: float) -> bool:
        if quote.delta is not None and self.rules.target_delta is not None:
            return abs(quote.delta - self.rules.target_delta) <= self.rules.delta_tolerance
        if self.rules.target_moneyness is None:
            return True
        moneyness = quote.strike / underlying_price
        return abs(moneyness - self.rules.target_moneyness) <= self.rules.moneyness_tolerance

    def _target_distance(self, quote: OptionQuote, underlying_price: float) -> float:
        if quote.delta is not None and self.rules.target_delta is not None:
            return abs(quote.delta - self.rules.target_delta)
        if self.rules.target_moneyness is not None:
            return abs((quote.strike / underlying_price) - self.rules.target_moneyness)
        return 0.0

    @staticmethod
    def _dte(quote: OptionQuote, quote_date: date) -> int:
        return (quote.expiry - quote_date).days


def implied_move_from_atm_straddle(
    quotes: Iterable[OptionQuote], underlying_price: float
) -> Optional[float]:
    grouped = {}
    for quote in quotes:
        grouped.setdefault(quote.strike, {})[quote.option_type.lower()] = quote
    complete = [
        (abs(strike - underlying_price), legs["call"], legs["put"])
        for strike, legs in grouped.items()
        if "call" in legs and "put" in legs
    ]
    if not complete or underlying_price <= 0:
        return None
    _, call, put = sorted(complete, key=lambda item: item[0])[0]
    return round((call.mid + put.mid) / underlying_price, 6)


def quotes_for_contract(quotes: List[OptionQuote], selected: OptionQuote, quote_date: date) -> Optional[OptionQuote]:
    for quote in quotes:
        if (
            quote.ticker == selected.ticker
            and quote.quote_date == quote_date
            and quote.expiry == selected.expiry
            and quote.option_type == selected.option_type
            and quote.strike == selected.strike
        ):
            return quote
    return None
