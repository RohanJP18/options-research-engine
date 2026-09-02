from __future__ import annotations

from .models import MetricSummary, OpportunityScore, ScoreWeights


def score_strategy(
    metrics: MetricSummary,
    weights: ScoreWeights = ScoreWeights(),
    avg_implied_vs_realized_edge: float = 0.0,
    min_samples: int = 20,
) -> OpportunityScore:
    components = {
        "expectancy": weights.expectancy * _clip(metrics.expectancy / 0.20),
        "win_rate": weights.win_rate * _clip(metrics.win_rate),
        "drawdown": weights.drawdown * _clip(1 - abs(metrics.max_drawdown) / 0.50),
        "sample_size": weights.sample_size * _clip(metrics.sample_size / min_samples),
        "implied_vs_realized": weights.implied_vs_realized
        * _clip(avg_implied_vs_realized_edge / 0.0909090909),
    }
    total = round(sum(components.values()), 6)
    return OpportunityScore(
        total=total,
        components={key: round(value, 6) for key, value in components.items()},
        explanation=(
            "Transparent weighted formula: expectancy, win rate, drawdown control, "
            "sample size, and average realized-minus-implied move are normalized to "
            "0..1 and multiplied by configured weights."
        ),
    )


def _clip(value: float) -> float:
    return max(0.0, min(1.0, value))
