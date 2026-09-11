from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
import requests
import yfinance as yf

from .live_scan import (
    LiveOptionCandidate,
    LiveScanConfig,
    build_underlying_snapshot,
    score_live_call,
    select_strategy_expiries,
    write_live_scan_report,
)
from .universe import load_public_us_listings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a broad live U.S. options scan.")
    parser.add_argument("--max-contract-cost", type=float, default=3000)
    parser.add_argument("--min-score", type=float, default=75)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--include-etfs", action="store_true")
    parser.add_argument("--max-underlyings", type=int, default=0)
    parser.add_argument("--chunk-size", type=int, default=150)
    parser.add_argument("--sleep", type=float, default=0.15)
    parser.add_argument("--option-workers", type=int, default=8)
    parser.add_argument("--output", default="outputs/broad_market_live_scan.md")
    args = parser.parse_args()

    config = LiveScanConfig(
        as_of=date.today(),
        max_contract_cost=args.max_contract_cost,
        min_score=args.min_score,
        top=args.top,
    )
    listings = load_public_us_listings(_http_get, include_etfs=args.include_etfs)
    symbols = [listing.yahoo_symbol for listing in listings]
    print(f"Loaded {len(symbols)} public U.S. listings after listing-type filters.")

    snapshots = _fetch_filtered_underlyings(symbols, config, args.chunk_size)
    snapshots = sorted(snapshots.values(), key=lambda row: row.avg_dollar_volume_20d, reverse=True)
    if args.max_underlyings > 0:
        snapshots = snapshots[: args.max_underlyings]
    print(f"{len(snapshots)} underlyings passed price/history/dollar-volume filters.")

    candidates = _scan_options_concurrently(
        snapshots=snapshots,
        config=config,
        workers=args.option_workers,
        sleep=args.sleep,
    )

    ranked = _dedupe_best_per_ticker_strategy(candidates)
    ranked = sorted(ranked, key=lambda item: item.score, reverse=True)[: args.top]
    source_note = (
        f"As of {config.as_of.isoformat()}. Universe source: Nasdaq Trader listed-symbol "
        f"directories plus Yahoo Finance price/options data. Filters: max cost "
        f"${config.max_contract_cost:,.0f}, min score {config.min_score}, min underlying "
        f"20d dollar volume ${config.min_avg_dollar_volume_20d:,.0f}."
    )
    report = write_live_scan_report(ranked, source_note, Path(args.output))
    print(report)


def _http_get(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _fetch_filtered_underlyings(
    symbols: Iterable[str],
    config: LiveScanConfig,
    chunk_size: int,
) -> Dict[str, object]:
    snapshots = {}
    symbol_list = list(symbols)
    for start in range(0, len(symbol_list), chunk_size):
        chunk = symbol_list[start : start + chunk_size]
        print(f"Fetching price history {start + 1}-{start + len(chunk)} of {len(symbol_list)}")
        try:
            downloaded = yf.download(
                tickers=chunk,
                period="6mo",
                interval="1d",
                auto_adjust=False,
                group_by="ticker",
                progress=False,
                threads=True,
            )
        except Exception as exc:
            print(f"Price chunk failed: {type(exc).__name__}: {exc}")
            continue
        for symbol in chunk:
            history = _history_for_symbol(downloaded, symbol, len(chunk))
            snapshot = build_underlying_snapshot(symbol, history)
            if snapshot is None:
                continue
            if (
                snapshot.price >= config.min_underlying_price
                and snapshot.avg_dollar_volume_20d >= config.min_avg_dollar_volume_20d
            ):
                snapshots[symbol] = snapshot
    return snapshots


def _history_for_symbol(downloaded: pd.DataFrame, symbol: str, chunk_len: int) -> pd.DataFrame:
    if downloaded.empty:
        return pd.DataFrame()
    if chunk_len == 1:
        return downloaded.copy()
    if not isinstance(downloaded.columns, pd.MultiIndex):
        return pd.DataFrame()
    if symbol not in downloaded.columns.get_level_values(0):
        return pd.DataFrame()
    return downloaded[symbol].copy()


def _scan_symbol_options(snapshot, config: LiveScanConfig) -> List[LiveOptionCandidate]:
    ticker = yf.Ticker(snapshot.ticker)
    expiries = select_strategy_expiries(
        [date.fromisoformat(expiry) for expiry in ticker.options],
        config,
    )
    candidates: List[LiveOptionCandidate] = []
    for expiry in expiries:
        try:
            calls = ticker.option_chain(expiry.isoformat()).calls
        except Exception:
            continue
        for _, row in calls.iterrows():
            candidate = score_live_call(snapshot, row, expiry, config)
            if candidate is not None:
                candidates.append(candidate)
    return candidates


def _scan_options_concurrently(
    snapshots,
    config: LiveScanConfig,
    workers: int,
    sleep: float,
) -> List[LiveOptionCandidate]:
    candidates: List[LiveOptionCandidate] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {}
        for snapshot in snapshots:
            future = executor.submit(_scan_symbol_options, snapshot, config)
            futures[future] = snapshot
            time.sleep(sleep)
        for idx, future in enumerate(as_completed(futures), start=1):
            snapshot = futures[future]
            if idx % 25 == 0 or idx == 1:
                print(f"Completed option chains {idx}/{len(futures)}: {snapshot.ticker}")
            try:
                candidates.extend(future.result())
            except Exception as exc:
                print(f"Skipped {snapshot.ticker}: {type(exc).__name__}: {exc}")
    return candidates


def _dedupe_best_per_ticker_strategy(
    candidates: Iterable[LiveOptionCandidate],
) -> List[LiveOptionCandidate]:
    best = {}
    for candidate in candidates:
        key = (candidate.ticker, candidate.strategy)
        if key not in best or candidate.score > best[key].score:
            best[key] = candidate
    return list(best.values())


if __name__ == "__main__":
    main()
