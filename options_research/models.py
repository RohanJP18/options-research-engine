from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

import pandas as pd


@dataclass(frozen=True)
class EarningsEvent:
    ticker: str
    event_date: date
    timing: str = "postmarket"
    announced_on: Optional[date] = None


@dataclass(frozen=True)
class AlignedEvent:
    event: EarningsEvent
    announcement_session: date
    last_pre_event_session: date
    first_post_event_session: date


@dataclass(frozen=True)
class OptionQuote:
    ticker: str
    quote_date: date
    expiry: date
    option_type: str
    strike: float
    bid: float
    ask: float
    delta: Optional[float]
    volume: int
    open_interest: int

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def spread_pct(self) -> float:
        if self.mid <= 0:
            return float("inf")
        return (self.ask - self.bid) / self.mid

    @property
    def contract_id(self) -> str:
        return f"{self.ticker}-{self.expiry.isoformat()}-{self.option_type}-{self.strike:g}"


@dataclass(frozen=True)
class ContractSelectionRules:
    min_dte: int
    max_dte: int
    target_delta: Optional[float] = 0.55
    delta_tolerance: float = 0.15
    target_moneyness: Optional[float] = None
    moneyness_tolerance: float = 0.10
    min_volume: int = 50
    min_open_interest: int = 100
    max_spread_pct: float = 0.30
    prefer_expiry_after_event: bool = True


@dataclass(frozen=True)
class ExecutionAssumptions:
    slippage_bps: float = 25
    contracts: int = 1
    multiplier: int = 100


@dataclass(frozen=True)
class PnlResult:
    entry_debit: float
    exit_credit: float
    pnl_dollars: float
    return_pct: float


@dataclass(frozen=True)
class MetricSummary:
    sample_size: int
    win_rate: float
    mean_return: float
    median_return: float
    max_drawdown: float
    expectancy: float

    @classmethod
    def empty(cls) -> "MetricSummary":
        return cls(
            sample_size=0,
            win_rate=0.0,
            mean_return=0.0,
            median_return=0.0,
            max_drawdown=0.0,
            expectancy=0.0,
        )


@dataclass(frozen=True)
class ScoreWeights:
    expectancy: float = 35
    win_rate: float = 20
    drawdown: float = 20
    sample_size: float = 15
    implied_vs_realized: float = 10


@dataclass(frozen=True)
class OpportunityScore:
    total: float
    components: Dict[str, float]
    explanation: str


@dataclass(frozen=True)
class BacktestTrade:
    ticker: str
    strategy: str
    event_date: Optional[date]
    entry_date: date
    exit_date: date
    contract_id: str
    entry_price: float
    exit_price: float
    return_pct: float
    pnl_dollars: float
    pre_earnings_return: Optional[float] = None
    post_earnings_return: Optional[float] = None
    implied_move: Optional[float] = None
    realized_move: Optional[float] = None
    implied_vs_realized: Optional[float] = None


@dataclass(frozen=True)
class StrategyBacktest:
    ticker: str
    strategy: str
    trades: List[BacktestTrade]
    metrics: MetricSummary
    skipped: List[Dict[str, str]] = field(default_factory=list)
    assumptions: Dict[str, str] = field(default_factory=dict)
    score: Optional[OpportunityScore] = None


@dataclass(frozen=True)
class DataBundle:
    prices: pd.DataFrame
    events: List[EarningsEvent]
    options: List[OptionQuote]
    source: str
    notes: str
