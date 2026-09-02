from __future__ import annotations

from .models import ExecutionAssumptions, OptionQuote, PnlResult


def long_option_pnl(
    entry_quote: OptionQuote, exit_quote: OptionQuote, assumptions: ExecutionAssumptions
) -> PnlResult:
    slippage = assumptions.slippage_bps / 10_000
    entry_debit = entry_quote.ask * (1 + slippage)
    exit_credit = exit_quote.bid * (1 - slippage)
    pnl_per_share = exit_credit - entry_debit
    pnl_dollars = pnl_per_share * assumptions.multiplier * assumptions.contracts
    return_pct = pnl_per_share / entry_debit if entry_debit else 0.0
    return PnlResult(
        entry_debit=round(entry_debit, 6),
        exit_credit=round(exit_credit, 6),
        pnl_dollars=round(pnl_dollars, 6),
        return_pct=round(return_pct, 6),
    )
