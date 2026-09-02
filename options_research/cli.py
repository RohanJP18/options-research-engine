from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .fixtures import load_fixture_bundle
from .report import generate_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run options research backtests.")
    parser.add_argument("--tickers", nargs="+", default=["NVDA", "TSLA", "ORCL", "AMD", "META"])
    parser.add_argument("--start", default="2023-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--output", default="outputs/options_research_report.md")
    args = parser.parse_args()

    bundle = load_fixture_bundle()
    report = generate_report(
        bundle=bundle,
        tickers=args.tickers,
        start=date.fromisoformat(args.start),
        end=date.fromisoformat(args.end),
        output_path=Path(args.output),
    )
    print(report.markdown)


if __name__ == "__main__":
    main()
