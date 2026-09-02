# Options Research Engine

A small, test-driven Python research engine for long-call option studies around earnings.
It implements the strategy family from the referenced conversation without assuming that
stocks rise into earnings. The engine measures that behavior per ticker, event, window,
and contract-selection rule.

## What It Researches

- `long_dated_call_LEAPS_E-30_to_E-1`: buy a long-dated call roughly 30 trading sessions before earnings and exit before the event.
- `pre_earnings_long_call_E-{30,20,10,5}_to_E-1`: buy a call before earnings and exit the trading session before the event.
- `earnings_event_long_call`: buy before the event and exit on the first post-earnings trading session.

The pre-earnings windows cover E-30, E-20, E-10, and E-5 through E-1.

## Setup

```bash
python3 -m pip install -e ".[dev]"
```

The current implementation uses `pandas`, `numpy`, and `pytest`. The engine is structured
so real historical option-chain adapters can be added without changing the strategy code.

## Test Suite

```bash
python3 -m pytest -q
```

Current verified result:

```text
11 passed
```

The tests were written before implementation and cover:

- Earnings date alignment for post-market and pre-market reports.
- No-future-leakage checks for event knowledge and quote dates.
- Contract selection by DTE, delta/moneyness, liquidity, spread, and expiry after earnings.
- Long-option P&L using bid/ask plus slippage.
- Implied move from ATM straddle quotes.
- Missing option-chain behavior.
- Transparent opportunity scoring.
- End-to-end report generation.

## Run A Backtest

```bash
python3 -m options_research.cli \
  --tickers NVDA TSLA ORCL AMD META \
  --start 2023-01-01 \
  --end 2024-12-31 \
  --output outputs/options_research_report.md
```

This writes a ranked markdown report and also prints it to the terminal.

## Architecture

- `options_research/events.py`: aligns events to tradable sessions and enforces no-lookahead checks.
- `options_research/options.py`: contract selection and implied-move calculations.
- `options_research/execution.py`: bid/ask/slippage-aware long-option execution.
- `options_research/metrics.py`: win rate, mean/median return, max drawdown, expectancy, and sample size.
- `options_research/scoring.py`: transparent weighted opportunity scores.
- `options_research/strategies/`: modular strategy implementations.
- `options_research/fixtures.py`: deterministic fixture prices, earnings, and option chains.
- `options_research/report.py`: ranked markdown report generation.
- `tests/`: TDD coverage for the core behavior.

## Methodology And Anti-Bias Safeguards

- Events must be known by the entry date when `announced_on` is provided.
- Option quotes after the entry date are not eligible for contract selection.
- Pre-earnings exits occur before the earnings event, avoiding accidental event exposure.
- Post-earnings realized move is measured only after the event session is reached.
- Option trades buy at ask plus slippage and sell at bid minus slippage.
- Missing option-chain or missing exit-quote cases are skipped with explicit reasons.
- Opportunity scores are weighted formulas, not opaque judgments.

## Data Limitation

The included backtest uses deterministic fixture data because reliable historical option
chains were not available in the environment. The fixture covers representative NVDA,
TSLA, ORCL, AMD, and META earnings cases and is useful for validating methodology and
software behavior. It is not market evidence and should not be interpreted as proof of
profitability.

To use real data, add a new `DataBundle` adapter that supplies:

- Underlying OHLC rows with `ticker`, `date`, `open`, and `close`.
- `EarningsEvent` records with event date, timing, and preferably `announced_on`.
- Historical `OptionQuote` records with quote date, expiry, strike, bid, ask, delta,
  volume, and open interest.

## Example Output

From the current fixture run:

```text
Strategy                                  Samples  Avg Win Rate  Avg Mean Return
long_dated_call_LEAPS_E-30_to_E-1          20       100.0%        42.2%
pre_earnings_long_call_E-30_to_E-1         20       100.0%       101.2%
pre_earnings_long_call_E-20_to_E-1         20        90.0%        48.7%
pre_earnings_long_call_E-10_to_E-1         20        80.0%        14.0%
pre_earnings_long_call_E-5_to_E-1          20        45.0%         0.6%
earnings_event_long_call                   20        80.0%        23.8%
```

These numbers are from deterministic fixtures only.
