from __future__ import annotations

from statistics import mean, median
from typing import Iterable, List

from .models import MetricSummary


def summarize_returns(returns: Iterable[float]) -> MetricSummary:
    values = list(returns)
    if not values:
        return MetricSummary.empty()
    wins = [value for value in values if value > 0]
    return MetricSummary(
        sample_size=len(values),
        win_rate=round(len(wins) / len(values), 6),
        mean_return=round(mean(values), 6),
        median_return=round(median(values), 6),
        max_drawdown=round(_max_drawdown(values), 6),
        expectancy=round(mean(values), 6),
    )


def _max_drawdown(returns: List[float]) -> float:
    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    for value in returns:
        equity *= 1 + value
        peak = max(peak, equity)
        drawdown = (equity / peak) - 1
        max_dd = min(max_dd, drawdown)
    return max_dd
