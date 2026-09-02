from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List, Optional

from .models import DataBundle, StrategyBacktest
from .strategies import run_all_strategies


@dataclass(frozen=True)
class ResearchReport:
    results: List[StrategyBacktest]
    markdown: str


def generate_report(
    bundle: DataBundle,
    tickers: Iterable[str],
    start: date,
    end: date,
    output_path: Optional[Path] = None,
) -> ResearchReport:
    ticker_list = [ticker.upper() for ticker in tickers]
    results = run_all_strategies(bundle, ticker_list, start, end)
    markdown = _render_markdown(bundle, ticker_list, start, end, results)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown)
    return ResearchReport(results=results, markdown=markdown)


def _render_markdown(
    bundle: DataBundle,
    tickers: List[str],
    start: date,
    end: date,
    results: List[StrategyBacktest],
) -> str:
    lines = [
        "# Options Research Report",
        "",
        f"Date range: {start.isoformat()} to {end.isoformat()}",
        f"Tickers: {', '.join(tickers)}",
        f"Data source: {bundle.source}",
        "",
        "## Methodology Guardrails",
        "",
        "- Earnings events are filtered to the requested date range before strategy evaluation.",
        "- A trade can only use an earnings event if its announced date is on or before entry.",
        "- Option selection uses the quote chain from the entry session only.",
        "- Long calls buy at ask plus slippage and sell at bid minus slippage.",
        "- Missing option chains, missing exits, or failed liquidity filters are reported as skipped cases.",
        "- Scores are transparent weighted sums; they are not model or LLM recommendations.",
        "",
        "## Ranked Opportunities",
        "",
        "| Rank | Ticker | Strategy | Score | Samples | Win Rate | Mean Return | Median Return | Max Drawdown | Skipped |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, result in enumerate(results, start=1):
        m = result.metrics
        lines.append(
            "| {rank} | {ticker} | {strategy} | {score:.2f} | {samples} | {win_rate:.1%} | "
            "{mean:.1%} | {median:.1%} | {drawdown:.1%} | {skipped} |".format(
                rank=rank,
                ticker=result.ticker,
                strategy=result.strategy,
                score=result.score.total if result.score else 0.0,
                samples=m.sample_size,
                win_rate=m.win_rate,
                mean=m.mean_return,
                median=m.median_return,
                drawdown=m.max_drawdown,
                skipped=len(result.skipped),
            )
        )

    lines.extend(
        [
            "",
            "## Strategy Details",
            "",
        ]
    )
    for result in results:
        m = result.metrics
        lines.extend(
            [
                f"### {result.ticker} - {result.strategy}",
                "",
                f"Score: {(result.score.total if result.score else 0.0):.2f}",
                f"Samples: {m.sample_size}",
                f"Win rate: {m.win_rate:.1%}",
                f"Mean / median return: {m.mean_return:.1%} / {m.median_return:.1%}",
                f"Max drawdown: {m.max_drawdown:.1%}",
                f"Expectancy: {m.expectancy:.1%}",
                "",
                "| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        if result.trades:
            for trade in result.trades:
                lines.append(
                    "| {event} | {entry} | {exit} | {contract} | {ret:.1%} | ${pnl:.2f} | {pre} | {post} | {imp} | {edge} |".format(
                        event=trade.event_date.isoformat() if trade.event_date else "",
                        entry=trade.entry_date.isoformat(),
                        exit=trade.exit_date.isoformat(),
                        contract=trade.contract_id,
                        ret=trade.return_pct,
                        pnl=trade.pnl_dollars,
                        pre=_pct(trade.pre_earnings_return),
                        post=_pct(trade.post_earnings_return),
                        imp=_pct(trade.implied_move),
                        edge=_pct(trade.implied_vs_realized),
                    )
                )
        else:
            lines.append("| No completed trades | | | | | | | | | |")
        if result.skipped:
            lines.extend(["", "Skipped cases:"])
            for skipped in result.skipped:
                lines.append(
                    f"- {skipped['event_date']}: {skipped['reason']} ({skipped['detail']})"
                )
        lines.append("")

    lines.extend(
        [
            "## Limitations",
            "",
            (
                "This report uses fixture data when historical option chains are unavailable. "
                "Fixture results test the engine and methodology; they do not establish a live trading edge."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _pct(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value:.1%}"
