from datetime import date

import pytest

from options_research.models import MetricSummary, ScoreWeights, StrategyBacktest
from options_research.scoring import score_strategy


def test_missing_option_data_is_explicitly_reported_not_silently_priced():
    result = StrategyBacktest(
        ticker="XYZ",
        strategy="earnings_event_long_call",
        trades=[],
        metrics=MetricSummary.empty(),
        skipped=[
            {
                "ticker": "XYZ",
                "event_date": "2024-02-21",
                "reason": "missing_option_chain",
            }
        ],
        assumptions={"data_source": "fixture"},
    )

    assert result.metrics.sample_size == 0
    assert result.skipped[0]["reason"] == "missing_option_chain"


def test_opportunity_score_is_transparent_weighted_sum():
    metrics = MetricSummary(
        sample_size=12,
        win_rate=0.58,
        mean_return=0.12,
        median_return=0.08,
        max_drawdown=-0.20,
        expectancy=0.12,
    )
    weights = ScoreWeights(
        expectancy=40,
        win_rate=20,
        drawdown=20,
        sample_size=10,
        implied_vs_realized=10,
    )

    score = score_strategy(
        metrics,
        weights,
        avg_implied_vs_realized_edge=0.04,
        min_samples=20,
    )

    assert score.total == pytest.approx(58.0)
    assert score.components["expectancy"] == pytest.approx(24.0)
    assert score.components["sample_size"] == pytest.approx(6.0)
    assert "weighted formula" in score.explanation
