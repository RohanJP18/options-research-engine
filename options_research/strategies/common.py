from __future__ import annotations

from dataclasses import replace
from datetime import date
from typing import Callable, Dict, Iterable, List, Optional, Tuple

from options_research.events import EventEngine
from options_research.execution import long_option_pnl
from options_research.metrics import summarize_returns
from options_research.models import (
    BacktestTrade,
    ContractSelectionRules,
    DataBundle,
    EarningsEvent,
    ExecutionAssumptions,
    MetricSummary,
    ScoreWeights,
    StrategyBacktest,
)
from options_research.options import ContractSelector, implied_move_from_atm_straddle, quotes_for_contract
from options_research.scoring import score_strategy

EntryExitFn = Callable[[EventEngine, EarningsEvent], Tuple[date, date]]


def backtest_event_long_call(
    bundle: DataBundle,
    ticker: str,
    strategy_name: str,
    start: date,
    end: date,
    rules: ContractSelectionRules,
    entry_exit: EntryExitFn,
    assumptions: ExecutionAssumptions = ExecutionAssumptions(),
) -> StrategyBacktest:
    engine = EventEngine(bundle.prices)
    events = _events_for(bundle.events, ticker, start, end)
    selector = ContractSelector(rules)
    trades: List[BacktestTrade] = []
    skipped: List[Dict[str, str]] = []

    for event in events:
        try:
            entry_date, exit_date = entry_exit(engine, event)
            aligned = engine.align_event(event)
        except (ValueError, KeyError) as exc:
            skipped.append(_skip(event, "insufficient_price_history", str(exc)))
            continue

        if not engine.event_is_known_by(event, entry_date):
            skipped.append(_skip(event, "event_not_known_by_entry", f"announced_on={event.announced_on}"))
            continue

        try:
            underlying_entry = engine.price_on(ticker, entry_date)
            pre_return = (
                engine.price_on(ticker, aligned.last_pre_event_session) / underlying_entry - 1
            )
            post_return = (
                engine.price_on(ticker, aligned.first_post_event_session)
                / engine.price_on(ticker, aligned.last_pre_event_session)
                - 1
            )
        except KeyError as exc:
            skipped.append(_skip(event, "missing_underlying_price", str(exc)))
            continue

        entry_quotes = [
            quote for quote in bundle.options if quote.ticker == ticker and quote.quote_date == entry_date
        ]
        if not entry_quotes:
            skipped.append(_skip(event, "missing_option_chain", f"quote_date={entry_date}"))
            continue

        selected = selector.select(
            entry_quotes,
            ticker=ticker,
            quote_date=entry_date,
            underlying_price=underlying_entry,
            event_date=event.event_date if rules.prefer_expiry_after_event else None,
        )
        if selected is None:
            skipped.append(_skip(event, "no_contract_passing_filters", f"quote_date={entry_date}"))
            continue

        exit_quote = quotes_for_contract(bundle.options, selected, exit_date)
        if exit_quote is None:
            skipped.append(
                _skip(
                    event,
                    "missing_exit_quote",
                    f"contract={selected.contract_id}, exit_date={exit_date}",
                )
            )
            continue

        pnl = long_option_pnl(selected, exit_quote, assumptions)
        same_expiry_quotes = [quote for quote in entry_quotes if quote.expiry == selected.expiry]
        implied_move = implied_move_from_atm_straddle(same_expiry_quotes, underlying_entry)
        realized_move = abs(post_return) if event.event_date is not None else None
        trades.append(
            BacktestTrade(
                ticker=ticker,
                strategy=strategy_name,
                event_date=event.event_date,
                entry_date=entry_date,
                exit_date=exit_date,
                contract_id=selected.contract_id,
                entry_price=pnl.entry_debit,
                exit_price=pnl.exit_credit,
                return_pct=pnl.return_pct,
                pnl_dollars=pnl.pnl_dollars,
                pre_earnings_return=round(pre_return, 6),
                post_earnings_return=round(post_return, 6),
                implied_move=implied_move,
                realized_move=round(realized_move, 6) if realized_move is not None else None,
                implied_vs_realized=round(realized_move - implied_move, 6)
                if implied_move is not None and realized_move is not None
                else None,
            )
        )

    metrics = summarize_returns(trade.return_pct for trade in trades)
    avg_edge = _mean(
        trade.implied_vs_realized for trade in trades if trade.implied_vs_realized is not None
    )
    score = score_strategy(metrics, ScoreWeights(), avg_edge)
    return StrategyBacktest(
        ticker=ticker,
        strategy=strategy_name,
        trades=trades,
        metrics=metrics,
        skipped=skipped,
        assumptions={
            "data_source": bundle.source,
            "slippage_bps": str(assumptions.slippage_bps),
            "contracts": str(assumptions.contracts),
            "multiplier": str(assumptions.multiplier),
            "min_dte": str(rules.min_dte),
            "max_dte": str(rules.max_dte),
            "target_delta": str(rules.target_delta),
            "max_spread_pct": str(rules.max_spread_pct),
            "min_volume": str(rules.min_volume),
            "min_open_interest": str(rules.min_open_interest),
        },
        score=score,
    )


def _events_for(
    events: Iterable[EarningsEvent], ticker: str, start: date, end: date
) -> List[EarningsEvent]:
    return sorted(
        [
            event
            for event in events
            if event.ticker == ticker and start <= event.event_date <= end
        ],
        key=lambda event: event.event_date,
    )


def _skip(event: EarningsEvent, reason: str, detail: str) -> Dict[str, str]:
    return {
        "ticker": event.ticker,
        "event_date": event.event_date.isoformat(),
        "reason": reason,
        "detail": detail,
    }


def _mean(values: Iterable[Optional[float]]) -> float:
    numbers = [value for value in values if value is not None]
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
