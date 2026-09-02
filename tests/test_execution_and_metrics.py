from datetime import date

import pytest

from options_research.execution import long_option_pnl
from options_research.metrics import summarize_returns
from options_research.models import ExecutionAssumptions, OptionQuote


def quote(bid, ask, quote_date=date(2024, 2, 14)):
    return OptionQuote(
        ticker="XYZ",
        quote_date=quote_date,
        expiry=date(2024, 3, 1),
        option_type="call",
        strike=100.0,
        bid=bid,
        ask=ask,
        delta=0.5,
        volume=100,
        open_interest=100,
    )


def test_long_option_pnl_applies_bid_ask_and_slippage():
    assumptions = ExecutionAssumptions(slippage_bps=100, contracts=1, multiplier=100)

    pnl = long_option_pnl(quote(5.0, 5.5), quote(7.8, 8.2), assumptions)

    assert pnl.entry_debit == pytest.approx(5.555)
    assert pnl.exit_credit == pytest.approx(7.722)
    assert pnl.pnl_dollars == pytest.approx(216.7)
    assert pnl.return_pct == pytest.approx(0.3901, abs=0.0001)


def test_metrics_include_expectancy_drawdown_and_sample_size():
    summary = summarize_returns([0.10, -0.05, 0.20, -0.10])

    assert summary.sample_size == 4
    assert summary.win_rate == 0.5
    assert summary.mean_return == pytest.approx(0.0375)
    assert summary.median_return == pytest.approx(0.025)
    assert summary.expectancy == pytest.approx(0.0375)
    assert summary.max_drawdown < 0
