from __future__ import annotations

from datetime import date

from options_research.events import EventEngine
from options_research.models import ContractSelectionRules, DataBundle, EarningsEvent, StrategyBacktest

from .common import backtest_event_long_call


def backtest_long_dated_calls(
    bundle: DataBundle, ticker: str, start: date, end: date
) -> StrategyBacktest:
    rules = ContractSelectionRules(
        min_dte=120,
        max_dte=760,
        target_delta=0.55,
        delta_tolerance=0.18,
        min_volume=100,
        min_open_interest=250,
        max_spread_pct=0.30,
        prefer_expiry_after_event=False,
    )
    return backtest_event_long_call(
        bundle,
        ticker,
        "long_dated_call_LEAPS_E-30_to_E-1",
        start,
        end,
        rules,
        _entry_exit,
    )


def _entry_exit(engine: EventEngine, event: EarningsEvent) -> tuple[date, date]:
    return engine.pre_event_window(event, 30)
