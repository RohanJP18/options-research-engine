from __future__ import annotations

from datetime import date
from typing import Iterable, List

from options_research.models import DataBundle, StrategyBacktest

from .earnings_event_long_call import backtest_earnings_event_long_call
from .long_dated_calls import backtest_long_dated_calls
from .pre_earnings_long_call import backtest_pre_earnings_long_call


def run_all_strategies(
    bundle: DataBundle, tickers: Iterable[str], start: date, end: date
) -> List[StrategyBacktest]:
    results: List[StrategyBacktest] = []
    for ticker in tickers:
        results.extend(
            [
                backtest_long_dated_calls(bundle, ticker, start, end),
                backtest_pre_earnings_long_call(bundle, ticker, start, end, window=30),
                backtest_pre_earnings_long_call(bundle, ticker, start, end, window=20),
                backtest_pre_earnings_long_call(bundle, ticker, start, end, window=10),
                backtest_pre_earnings_long_call(bundle, ticker, start, end, window=5),
                backtest_earnings_event_long_call(bundle, ticker, start, end),
            ]
        )
    return sorted(
        results,
        key=lambda result: result.score.total if result.score else 0.0,
        reverse=True,
    )
