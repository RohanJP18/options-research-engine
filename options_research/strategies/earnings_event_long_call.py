from __future__ import annotations

from datetime import date

from options_research.events import EventEngine
from options_research.models import ContractSelectionRules, DataBundle, EarningsEvent, StrategyBacktest

from .common import backtest_event_long_call


def backtest_earnings_event_long_call(
    bundle: DataBundle, ticker: str, start: date, end: date
) -> StrategyBacktest:
    rules = ContractSelectionRules(
        min_dte=2,
        max_dte=45,
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
        "earnings_event_long_call",
        start,
        end,
        rules,
        _entry_exit,
    )


def _entry_exit(engine: EventEngine, event: EarningsEvent) -> tuple[date, date]:
    aligned = engine.align_event(event)
    return aligned.last_pre_event_session, aligned.first_post_event_session
