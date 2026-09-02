from __future__ import annotations

from datetime import date

from options_research.events import EventEngine
from options_research.models import ContractSelectionRules, DataBundle, EarningsEvent, StrategyBacktest

from .common import backtest_event_long_call


def backtest_pre_earnings_long_call(
    bundle: DataBundle, ticker: str, start: date, end: date, window: int = 20
) -> StrategyBacktest:
    rules = ContractSelectionRules(
        min_dte=5,
        max_dte=75,
        target_delta=0.55,
        delta_tolerance=0.15,
        min_volume=100,
        min_open_interest=250,
        max_spread_pct=0.25,
        prefer_expiry_after_event=True,
    )
    return backtest_event_long_call(
        bundle,
        ticker,
        f"pre_earnings_long_call_E-{window}_to_E-1",
        start,
        end,
        rules,
        lambda engine, event: _entry_exit(engine, event, window),
    )


def _entry_exit(engine: EventEngine, event: EarningsEvent, window: int) -> tuple[date, date]:
    return engine.pre_event_window(event, window)
