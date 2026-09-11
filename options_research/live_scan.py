from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import log, sqrt
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class UnderlyingSnapshot:
    ticker: str
    price: float
    avg_volume_20d: float
    avg_dollar_volume_20d: float
    return_5d: float
    return_20d: float
    return_60d: float
    realized_vol_20d: Optional[float]
    realized_vol_60d: Optional[float]


@dataclass(frozen=True)
class LiveScanConfig:
    as_of: date
    max_contract_cost: float = 3_000
    min_underlying_price: float = 5
    min_avg_dollar_volume_20d: float = 25_000_000
    min_option_volume: int = 50
    min_open_interest: int = 250
    min_premium_volume: float = 25_000
    max_spread_pct: float = 0.25
    min_dte: int = 14
    max_dte: int = 760
    leap_min_dte: int = 300
    leap_max_dte: int = 760
    target_moneyness: float = 1.05
    max_moneyness: float = 1.25
    min_score: float = 75
    top: int = 50
    target_dtes: Tuple[int, ...] = (30, 60, 90, 120, 365, 540, 730)


@dataclass(frozen=True)
class LiveOptionCandidate:
    ticker: str
    strategy: str
    expiry: date
    strike: float
    option_type: str
    bid: float
    ask: float
    volume: int
    open_interest: int
    implied_volatility: Optional[float]
    underlying: UnderlyingSnapshot
    score: float
    components: dict
    reason: str

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def total_cost(self) -> float:
        return self.ask * 100

    @property
    def spread_pct(self) -> float:
        if self.mid <= 0:
            return float("inf")
        return (self.ask - self.bid) / self.mid

    @property
    def premium_volume(self) -> float:
        return self.volume * self.mid * 100

    @property
    def dte(self) -> int:
        return (self.expiry - self.components["as_of"]).days

    @property
    def breakeven_pct(self) -> float:
        return (self.strike + self.ask) / self.underlying.price - 1


def build_underlying_snapshot(ticker: str, history: pd.DataFrame) -> Optional[UnderlyingSnapshot]:
    if history.empty or "Close" not in history or "Volume" not in history:
        return None
    data = history.dropna(subset=["Close", "Volume"]).copy()
    if len(data) < 65:
        return None
    price = float(data["Close"].iloc[-1])
    avg_volume = float(data["Volume"].tail(20).mean())
    avg_dollar_volume = float((data["Close"] * data["Volume"]).tail(20).mean())
    return UnderlyingSnapshot(
        ticker=ticker,
        price=price,
        avg_volume_20d=avg_volume,
        avg_dollar_volume_20d=avg_dollar_volume,
        return_5d=_return_over(data["Close"], 5),
        return_20d=_return_over(data["Close"], 20),
        return_60d=_return_over(data["Close"], 60),
        realized_vol_20d=realized_volatility(data["Close"], 20),
        realized_vol_60d=realized_volatility(data["Close"], 60),
    )


def realized_volatility(closes: pd.Series, window: int) -> Optional[float]:
    values = closes.dropna().astype(float)
    if len(values) <= window:
        return None
    returns = np.log(values / values.shift(1)).dropna().tail(window)
    if len(returns) < window:
        return None
    return float(returns.std(ddof=1) * sqrt(252))


def score_live_call(
    underlying: UnderlyingSnapshot,
    option_row: pd.Series,
    expiry: date,
    config: LiveScanConfig,
) -> Optional[LiveOptionCandidate]:
    bid = _float_field(option_row.get("bid", 0))
    ask = _float_field(option_row.get("ask", 0))
    strike = _float_field(option_row.get("strike", 0))
    volume = _int_field(option_row.get("volume", 0))
    open_interest = _int_field(option_row.get("openInterest", 0))
    iv = option_row.get("impliedVolatility")
    iv = float(iv) if pd.notna(iv) else None
    if bid < 0 or ask <= 0 or ask < bid or strike <= 0:
        return None

    mid = (bid + ask) / 2
    spread_pct = (ask - bid) / mid if mid > 0 else float("inf")
    premium_volume = volume * mid * 100
    dte = (expiry - config.as_of).days
    moneyness = strike / underlying.price
    contract_cost = ask * 100

    if not (
        config.min_dte <= dte <= config.max_dte
        and contract_cost <= config.max_contract_cost
        and volume >= config.min_option_volume
        and open_interest >= config.min_open_interest
        and premium_volume >= config.min_premium_volume
        and spread_pct <= config.max_spread_pct
        and 0.85 <= moneyness <= config.max_moneyness
    ):
        return None

    strategy = "LEAPS_long_call" if config.leap_min_dte <= dte <= config.leap_max_dte else "momentum_long_call"
    liquidity_score = _score_liquidity(spread_pct, volume, open_interest, premium_volume)
    momentum_score = _score_momentum(underlying.return_5d, underlying.return_20d, underlying.return_60d)
    contract_score = _score_contract_fit(moneyness, dte, (strike + ask) / underlying.price - 1, strategy)
    volatility_score = _score_volatility_value(iv, underlying.realized_vol_20d, underlying.realized_vol_60d)
    trend_penalty = 0 if underlying.return_5d > -0.06 else -8

    components = {
        "as_of": config.as_of,
        "liquidity": liquidity_score,
        "momentum": momentum_score,
        "contract_fit": contract_score,
        "volatility_value": volatility_score,
        "trend_penalty": trend_penalty,
    }
    score = round(
        liquidity_score * 0.30
        + momentum_score * 0.25
        + contract_score * 0.25
        + volatility_score * 0.20
        + trend_penalty,
        1,
    )
    if score < config.min_score:
        return None

    reason = _reason(strategy, spread_pct, premium_volume, moneyness, iv, underlying)
    return LiveOptionCandidate(
        ticker=underlying.ticker,
        strategy=strategy,
        expiry=expiry,
        strike=strike,
        option_type="call",
        bid=bid,
        ask=ask,
        volume=volume,
        open_interest=open_interest,
        implied_volatility=iv,
        underlying=underlying,
        score=score,
        components=components,
        reason=reason,
    )


def render_live_scan_report(candidates: Iterable[LiveOptionCandidate], source_note: str) -> str:
    ranked = sorted(candidates, key=lambda item: item.score, reverse=True)
    lines = [
        "# Broad Market Live Options Scan",
        "",
        source_note,
        "",
        "| Rank | Ticker | Strategy | Contract | Score | Ask | Cost | Spread | Vol/OI | Premium Vol | IV | 5d/20d/60d | Reason |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- | --- |",
    ]
    for rank, candidate in enumerate(ranked, start=1):
        iv = "n/a" if candidate.implied_volatility is None else f"{candidate.implied_volatility:.1%}"
        lines.append(
            "| {rank} | {ticker} | {strategy} | {expiry} ${strike:g} call | {score:.1f} | "
            "${ask:.2f} | ${cost:.0f} | {spread:.1%} | {volume}/{oi} | ${premium_volume:,.0f} | "
            "{iv} | {r5:.1%}/{r20:.1%}/{r60:.1%} | {reason} |".format(
                rank=rank,
                ticker=candidate.ticker,
                strategy=candidate.strategy,
                expiry=candidate.expiry.isoformat(),
                strike=candidate.strike,
                score=candidate.score,
                ask=candidate.ask,
                cost=candidate.total_cost,
                spread=candidate.spread_pct,
                volume=candidate.volume,
                oi=candidate.open_interest,
                premium_volume=candidate.premium_volume,
                iv=iv,
                r5=candidate.underlying.return_5d,
                r20=candidate.underlying.return_20d,
                r60=candidate.underlying.return_60d,
                reason=candidate.reason,
            )
        )
    return "\n".join(lines) + "\n"


def write_live_scan_report(
    candidates: Iterable[LiveOptionCandidate],
    source_note: str,
    output_path: Path,
) -> str:
    report = render_live_scan_report(candidates, source_note)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    return report


def select_strategy_expiries(expiries: Iterable[date], config: LiveScanConfig) -> List[date]:
    valid = sorted(
        {
            expiry
            for expiry in expiries
            if config.min_dte <= (expiry - config.as_of).days <= config.max_dte
        }
    )
    selected = []
    for target_dte in config.target_dtes:
        if config.min_dte <= target_dte <= config.max_dte:
            closest = min(valid, key=lambda expiry: abs((expiry - config.as_of).days - target_dte), default=None)
            if closest is not None and closest not in selected:
                selected.append(closest)
    return sorted(selected)


def _return_over(closes: pd.Series, periods: int) -> float:
    if len(closes) <= periods:
        return 0.0
    start = float(closes.iloc[-(periods + 1)])
    end = float(closes.iloc[-1])
    if start <= 0:
        return 0.0
    return end / start - 1


def _float_field(value) -> float:
    if pd.isna(value):
        return 0.0
    return float(value)


def _int_field(value) -> int:
    if pd.isna(value):
        return 0
    return int(value)


def _score_liquidity(spread_pct: float, volume: int, open_interest: int, premium_volume: float) -> float:
    spread_points = 100 * max(0, min(1, (0.25 - spread_pct) / 0.25))
    volume_points = 100 * max(0, min(1, volume / 1_000))
    oi_points = 100 * max(0, min(1, open_interest / 5_000))
    premium_points = 100 * max(0, min(1, premium_volume / 250_000))
    return round(spread_points * 0.35 + volume_points * 0.20 + oi_points * 0.20 + premium_points * 0.25, 1)


def _score_momentum(return_5d: float, return_20d: float, return_60d: float) -> float:
    score = 50
    score += max(-20, min(20, return_5d * 250))
    score += max(-30, min(30, return_20d * 180))
    score += max(-20, min(20, return_60d * 100))
    return round(max(0, min(100, score)), 1)


def _score_contract_fit(moneyness: float, dte: int, breakeven_pct: float, strategy: str) -> float:
    moneyness_points = 100 * max(0, min(1, 1 - abs(moneyness - 1.05) / 0.20))
    breakeven_points = 100 * max(0, min(1, (0.30 - breakeven_pct) / 0.30))
    if strategy == "LEAPS_long_call":
        dte_points = 100 * max(0, min(1, 1 - abs(dte - 540) / 300))
    else:
        dte_points = 100 * max(0, min(1, 1 - abs(dte - 70) / 90))
    return round(moneyness_points * 0.35 + breakeven_points * 0.35 + dte_points * 0.30, 1)


def _score_volatility_value(
    implied_volatility: Optional[float],
    realized_vol_20d: Optional[float],
    realized_vol_60d: Optional[float],
) -> float:
    realized = realized_vol_20d or realized_vol_60d
    if implied_volatility is None or realized is None or realized <= 0:
        return 55.0
    ratio = implied_volatility / realized
    if ratio <= 0.85:
        return 95.0
    if ratio <= 1.10:
        return 80.0
    if ratio <= 1.35:
        return 65.0
    if ratio <= 1.75:
        return 45.0
    return 25.0


def _reason(
    strategy: str,
    spread_pct: float,
    premium_volume: float,
    moneyness: float,
    iv: Optional[float],
    underlying: UnderlyingSnapshot,
) -> str:
    iv_text = "IV unavailable" if iv is None else f"IV {iv:.1%}"
    return (
        f"{strategy.replace('_', ' ')}, {moneyness:.2f}x moneyness, "
        f"{spread_pct:.1%} spread, ${premium_volume:,.0f} premium flow, "
        f"{iv_text}, 20d momentum {underlying.return_20d:.1%}"
    )
