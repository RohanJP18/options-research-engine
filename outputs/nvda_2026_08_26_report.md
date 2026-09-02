# Options Research Report

Date range: 2026-08-01 to 2026-08-27
Tickers: NVDA
Data source: deterministic fixture data

## Methodology Guardrails

- Earnings events are filtered to the requested date range before strategy evaluation.
- A trade can only use an earnings event if its announced date is on or before entry.
- Option selection uses the quote chain from the entry session only.
- Long calls buy at ask plus slippage and sell at bid minus slippage.
- Missing option chains, missing exits, or failed liquidity filters are reported as skipped cases.
- Scores are transparent weighted sums; they are not model or LLM recommendations.

## Ranked Opportunities

| Rank | Ticker | Strategy | Score | Samples | Win Rate | Mean Return | Median Return | Max Drawdown | Skipped |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | NVDA | long_dated_call_LEAPS_E-30_to_E-1 | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |
| 2 | NVDA | pre_earnings_long_call_E-30_to_E-1 | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |
| 3 | NVDA | pre_earnings_long_call_E-20_to_E-1 | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |
| 4 | NVDA | pre_earnings_long_call_E-10_to_E-1 | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |
| 5 | NVDA | pre_earnings_long_call_E-5_to_E-1 | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |
| 6 | NVDA | earnings_event_long_call | 20.00 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | 0 |

## Strategy Details

### NVDA - long_dated_call_LEAPS_E-30_to_E-1

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

### NVDA - pre_earnings_long_call_E-30_to_E-1

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

### NVDA - pre_earnings_long_call_E-20_to_E-1

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

### NVDA - pre_earnings_long_call_E-10_to_E-1

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

### NVDA - pre_earnings_long_call_E-5_to_E-1

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

### NVDA - earnings_event_long_call

Score: 20.00
Samples: 0
Win rate: 0.0%
Mean / median return: 0.0% / 0.0%
Max drawdown: 0.0%
Expectancy: 0.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No completed trades | | | | | | | | | |

## Limitations

This report uses fixture data when historical option chains are unavailable. Fixture results test the engine and methodology; they do not establish a live trading edge.
