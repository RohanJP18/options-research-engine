from datetime import date

import pandas as pd

from options_research.live_scan import (
    LiveScanConfig,
    UnderlyingSnapshot,
    build_underlying_snapshot,
    render_live_scan_report,
    score_live_call,
    select_strategy_expiries,
)


def test_build_underlying_snapshot_uses_returns_and_annualized_log_volatility():
    history = pd.DataFrame(
        {
            "Close": [100 + idx for idx in range(80)],
            "Volume": [1_000_000 for _ in range(80)],
        }
    )

    snapshot = build_underlying_snapshot("XYZ", history)

    assert snapshot is not None
    assert snapshot.ticker == "XYZ"
    assert snapshot.price == 179
    assert snapshot.return_20d > 0
    assert snapshot.realized_vol_20d is not None


def test_live_call_scoring_filters_low_premium_volume_contracts():
    snapshot = _snapshot()
    config = LiveScanConfig(
        as_of=date(2026, 9, 11),
        min_premium_volume=50_000,
        min_score=0,
    )
    row = pd.Series(
        {
            "strike": 105.0,
            "bid": 0.20,
            "ask": 0.22,
            "volume": 1_000,
            "openInterest": 5_000,
            "impliedVolatility": 0.35,
        }
    )

    assert score_live_call(snapshot, row, date(2026, 11, 20), config) is None


def test_live_call_scoring_treats_missing_volume_as_illiquid():
    snapshot = _snapshot()
    config = LiveScanConfig(as_of=date(2026, 9, 11), min_score=0)
    row = pd.Series(
        {
            "strike": 105.0,
            "bid": 4.90,
            "ask": 5.10,
            "volume": float("nan"),
            "openInterest": 5_000,
            "impliedVolatility": 0.30,
        }
    )

    assert score_live_call(snapshot, row, date(2026, 11, 20), config) is None


def test_live_call_scoring_returns_transparent_components_and_report():
    snapshot = _snapshot()
    config = LiveScanConfig(as_of=date(2026, 9, 11), min_score=0)
    row = pd.Series(
        {
            "strike": 105.0,
            "bid": 4.90,
            "ask": 5.10,
            "volume": 400,
            "openInterest": 5_000,
            "impliedVolatility": 0.30,
        }
    )

    candidate = score_live_call(snapshot, row, date(2026, 11, 20), config)
    report = render_live_scan_report([candidate], "fixture source")

    assert candidate is not None
    assert candidate.components["liquidity"] > 0
    assert candidate.premium_volume == 200_000
    assert "Premium Vol" in report
    assert "XYZ" in report


def test_select_strategy_expiries_uses_nearest_playbook_horizons():
    config = LiveScanConfig(
        as_of=date(2026, 9, 11),
        target_dtes=(30, 365),
    )
    expiries = [
        date(2026, 9, 18),
        date(2026, 10, 9),
        date(2026, 10, 16),
        date(2027, 9, 17),
        date(2027, 12, 17),
    ]

    assert select_strategy_expiries(expiries, config) == [
        date(2026, 10, 9),
        date(2027, 9, 17),
    ]


def _snapshot() -> UnderlyingSnapshot:
    return UnderlyingSnapshot(
        ticker="XYZ",
        price=100.0,
        avg_volume_20d=2_000_000,
        avg_dollar_volume_20d=200_000_000,
        return_5d=0.02,
        return_20d=0.08,
        return_60d=0.12,
        realized_vol_20d=0.28,
        realized_vol_60d=0.25,
    )
