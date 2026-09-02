# Options Research Report

Date range: 2023-01-01 to 2024-12-31
Tickers: NVDA, TSLA, ORCL, AMD, META
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
| 1 | NVDA | long_dated_call_LEAPS_E-30_to_E-1 | 78.00 | 4 | 100.0% | 62.3% | 60.1% | 0.0% | 0 |
| 2 | NVDA | pre_earnings_long_call_E-30_to_E-1 | 78.00 | 4 | 100.0% | 138.9% | 148.9% | 0.0% | 0 |
| 3 | NVDA | pre_earnings_long_call_E-20_to_E-1 | 78.00 | 4 | 100.0% | 79.1% | 74.2% | 0.0% | 0 |
| 4 | NVDA | pre_earnings_long_call_E-10_to_E-1 | 78.00 | 4 | 100.0% | 25.0% | 27.8% | 0.0% | 0 |
| 5 | NVDA | earnings_event_long_call | 78.00 | 4 | 100.0% | 53.0% | 51.5% | 0.0% | 0 |
| 6 | TSLA | pre_earnings_long_call_E-30_to_E-1 | 78.00 | 4 | 100.0% | 53.6% | 57.1% | 0.0% | 0 |
| 7 | ORCL | long_dated_call_LEAPS_E-30_to_E-1 | 78.00 | 4 | 100.0% | 38.0% | 38.0% | 0.0% | 0 |
| 8 | ORCL | pre_earnings_long_call_E-30_to_E-1 | 78.00 | 4 | 100.0% | 85.7% | 94.0% | 0.0% | 0 |
| 9 | AMD | long_dated_call_LEAPS_E-30_to_E-1 | 78.00 | 4 | 100.0% | 44.3% | 42.2% | 0.0% | 0 |
| 10 | AMD | pre_earnings_long_call_E-30_to_E-1 | 78.00 | 4 | 100.0% | 111.8% | 108.6% | 0.0% | 0 |
| 11 | AMD | pre_earnings_long_call_E-20_to_E-1 | 78.00 | 4 | 100.0% | 51.5% | 49.4% | 0.0% | 0 |
| 12 | AMD | earnings_event_long_call | 78.00 | 4 | 100.0% | 27.1% | 26.6% | 0.0% | 0 |
| 13 | META | long_dated_call_LEAPS_E-30_to_E-1 | 78.00 | 4 | 100.0% | 49.2% | 48.3% | 0.0% | 0 |
| 14 | META | pre_earnings_long_call_E-30_to_E-1 | 78.00 | 4 | 100.0% | 116.1% | 98.6% | 0.0% | 0 |
| 15 | META | pre_earnings_long_call_E-20_to_E-1 | 78.00 | 4 | 100.0% | 55.6% | 46.1% | 0.0% | 0 |
| 16 | META | earnings_event_long_call | 78.00 | 4 | 100.0% | 45.5% | 45.5% | 0.0% | 0 |
| 17 | TSLA | long_dated_call_LEAPS_E-30_to_E-1 | 72.85 | 4 | 100.0% | 17.1% | 17.6% | 0.0% | 0 |
| 18 | ORCL | earnings_event_long_call | 72.42 | 4 | 100.0% | 16.8% | 15.1% | 0.0% | 0 |
| 19 | ORCL | pre_earnings_long_call_E-20_to_E-1 | 72.28 | 4 | 75.0% | 40.2% | 44.0% | -1.8% | 0 |
| 20 | META | pre_earnings_long_call_E-10_to_E-1 | 70.40 | 4 | 100.0% | 15.7% | 13.9% | 0.0% | 0 |
| 21 | AMD | pre_earnings_long_call_E-10_to_E-1 | 67.45 | 4 | 75.0% | 16.9% | 14.1% | -0.2% | 0 |
| 22 | TSLA | pre_earnings_long_call_E-20_to_E-1 | 66.73 | 4 | 75.0% | 17.1% | 11.8% | -3.1% | 0 |
| 23 | ORCL | pre_earnings_long_call_E-10_to_E-1 | 55.81 | 4 | 75.0% | 10.7% | 9.3% | -2.5% | 0 |
| 24 | NVDA | pre_earnings_long_call_E-5_to_E-1 | 45.13 | 4 | 75.0% | 4.8% | 6.4% | -3.2% | 0 |
| 25 | AMD | pre_earnings_long_call_E-5_to_E-1 | 33.82 | 4 | 50.0% | 2.3% | 2.2% | -8.2% | 0 |
| 26 | META | pre_earnings_long_call_E-5_to_E-1 | 31.90 | 4 | 50.0% | 1.3% | 0.2% | -8.4% | 0 |
| 27 | TSLA | pre_earnings_long_call_E-10_to_E-1 | 27.33 | 4 | 50.0% | 1.8% | -3.6% | -22.1% | 0 |
| 28 | ORCL | pre_earnings_long_call_E-5_to_E-1 | 23.31 | 4 | 25.0% | -1.0% | -2.9% | -11.7% | 0 |
| 29 | TSLA | pre_earnings_long_call_E-5_to_E-1 | 18.80 | 4 | 25.0% | -4.6% | -6.7% | -23.0% | 0 |
| 30 | TSLA | earnings_event_long_call | 3.00 | 4 | 0.0% | -23.3% | -24.6% | -65.9% | 0 |

## Strategy Details

### NVDA - long_dated_call_LEAPS_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 62.3% / 60.1%
Max drawdown: 0.0%
Expectancy: 62.3%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-01-11 | 2023-02-21 | NVDA-2024-01-19-call-171.38 | 26.0% | $1191.15 | 4.2% | 12.7% | 39.3% | -26.6% |
| 2023-05-24 | 2023-04-12 | 2023-05-23 | NVDA-2024-01-19-call-220.65 | 52.8% | $2564.29 | 7.9% | 13.1% | 32.8% | -19.7% |
| 2023-08-23 | 2023-07-12 | 2023-08-22 | NVDA-2024-01-19-call-282.01 | 102.7% | $5017.99 | 13.2% | 12.9% | 26.3% | -13.4% |
| 2024-02-21 | 2024-01-10 | 2024-02-20 | NVDA-2025-01-17-call-414.48 | 67.5% | $7463.99 | 13.1% | 11.8% | 39.3% | -27.5% |

### NVDA - pre_earnings_long_call_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 138.9% / 148.9%
Max drawdown: 0.0%
Expectancy: 138.9%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-01-11 | 2023-02-21 | NVDA-2023-02-24-call-171.38 | 78.6% | $1316.33 | 4.2% | 12.7% | 15.8% | -3.1% |
| 2023-05-24 | 2023-04-12 | 2023-05-23 | NVDA-2023-05-26-call-220.65 | 120.1% | $2588.74 | 7.9% | 13.1% | 15.8% | -2.8% |
| 2023-08-23 | 2023-07-12 | 2023-08-22 | NVDA-2023-08-25-call-282.01 | 179.1% | $4932.86 | 13.2% | 12.9% | 15.8% | -3.0% |
| 2024-02-21 | 2024-01-10 | 2024-02-20 | NVDA-2024-02-23-call-414.48 | 177.7% | $7194.72 | 13.1% | 11.8% | 15.8% | -4.0% |

### NVDA - pre_earnings_long_call_E-20_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 79.1% / 74.2%
Max drawdown: 0.0%
Expectancy: 79.1%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-01-25 | 2023-02-21 | NVDA-2023-02-24-call-171.38 | 52.3% | $1026.61 | 4.0% | 12.7% | 17.1% | -4.4% |
| 2023-05-24 | 2023-04-26 | 2023-05-23 | NVDA-2023-05-26-call-220.65 | 92.1% | $2274.95 | 8.4% | 13.1% | 16.9% | -3.9% |
| 2023-08-23 | 2023-07-26 | 2023-08-22 | NVDA-2023-08-25-call-282.01 | 115.8% | $4124.85 | 11.8% | 12.9% | 18.1% | -5.3% |
| 2024-02-21 | 2024-01-24 | 2024-02-20 | NVDA-2024-02-23-call-414.48 | 56.3% | $4049.88 | 7.4% | 11.8% | 22.0% | -10.2% |

### NVDA - pre_earnings_long_call_E-10_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 25.0% / 27.8%
Max drawdown: 0.0%
Expectancy: 25.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-02-08 | 2023-02-21 | NVDA-2023-02-24-call-171.38 | 24.0% | $578.49 | 3.0% | 12.7% | 19.2% | -6.5% |
| 2023-05-24 | 2023-05-10 | 2023-05-23 | NVDA-2023-05-26-call-220.65 | 37.4% | $1291.50 | 5.2% | 13.1% | 20.5% | -7.4% |
| 2023-08-23 | 2023-08-09 | 2023-08-22 | NVDA-2023-08-25-call-282.01 | 31.6% | $1845.16 | 5.9% | 12.9% | 24.4% | -11.6% |
| 2024-02-21 | 2024-02-07 | 2024-02-20 | NVDA-2024-02-23-call-414.48 | 7.0% | $733.61 | 2.0% | 11.8% | 27.8% | -16.0% |

### NVDA - earnings_event_long_call

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 53.0% / 51.5%
Max drawdown: 0.0%
Expectancy: 53.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-02-21 | 2023-02-23 | NVDA-2023-02-24-call-171.38 | 67.9% | $2212.18 | 0.0% | 12.7% | 23.1% | -10.3% |
| 2023-05-24 | 2023-05-23 | 2023-05-25 | NVDA-2023-05-26-call-220.65 | 57.6% | $2973.72 | 0.0% | 13.1% | 26.4% | -13.3% |
| 2023-08-23 | 2023-08-22 | 2023-08-24 | NVDA-2023-08-25-call-282.01 | 45.4% | $3801.62 | 0.0% | 12.9% | 30.7% | -17.8% |
| 2024-02-21 | 2024-02-20 | 2024-02-22 | NVDA-2024-02-23-call-414.48 | 41.2% | $5040.16 | 0.0% | 11.8% | 30.6% | -18.8% |

### TSLA - pre_earnings_long_call_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 53.6% / 57.1%
Max drawdown: 0.0%
Expectancy: 53.6%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2022-12-14 | 2023-01-24 | TSLA-2023-01-27-call-122.3 | 69.8% | $781.45 | 2.9% | -7.5% | 15.2% | -7.7% |
| 2023-04-19 | 2023-03-08 | 2023-04-18 | TSLA-2023-04-21-call-117.04 | 45.2% | $484.43 | 0.9% | -7.5% | 15.2% | -7.7% |
| 2023-10-18 | 2023-09-06 | 2023-10-17 | TSLA-2023-10-20-call-115.24 | 30.1% | $316.94 | -3.7% | -6.7% | 15.2% | -8.6% |
| 2024-01-24 | 2023-12-13 | 2024-01-23 | TSLA-2024-01-26-call-105.89 | 69.0% | $668.48 | 2.9% | -6.5% | 15.2% | -8.8% |

### ORCL - long_dated_call_LEAPS_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 38.0% / 38.0%
Max drawdown: 0.0%
Expectancy: 38.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-01-26 | 2023-03-08 | ORCL-2024-01-19-call-84.21 | 20.4% | $434.26 | 2.7% | 4.8% | 37.6% | -32.8% |
| 2023-06-12 | 2023-05-01 | 2023-06-09 | ORCL-2024-01-19-call-90.04 | 55.7% | $1023.25 | 7.8% | 4.3% | 30.8% | -26.5% |
| 2023-09-11 | 2023-07-31 | 2023-09-08 | ORCL-2024-01-19-call-98.6 | 70.6% | $1095.50 | 7.6% | 3.8% | 24.4% | -20.6% |
| 2024-03-11 | 2024-01-29 | 2024-03-08 | ORCL-2025-01-17-call-117.91 | 5.4% | $158.81 | -1.3% | 3.8% | 37.3% | -33.5% |

### ORCL - pre_earnings_long_call_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 85.7% / 94.0%
Max drawdown: 0.0%
Expectancy: 85.7%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-01-26 | 2023-03-08 | ORCL-2023-03-10-call-84.21 | 66.8% | $511.89 | 2.7% | 4.8% | 15.2% | -10.4% |
| 2023-06-12 | 2023-05-01 | 2023-06-09 | ORCL-2023-06-16-call-90.04 | 124.2% | $1033.25 | 7.8% | 4.3% | 15.4% | -11.1% |
| 2023-09-11 | 2023-07-31 | 2023-09-08 | ORCL-2023-09-15-call-98.6 | 121.1% | $1103.68 | 7.6% | 3.8% | 15.4% | -11.6% |
| 2024-03-11 | 2024-01-29 | 2024-03-08 | ORCL-2024-03-15-call-117.91 | 30.7% | $334.71 | -1.3% | 3.8% | 15.4% | -11.6% |

### AMD - long_dated_call_LEAPS_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 44.3% / 42.2%
Max drawdown: 0.0%
Expectancy: 44.3%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2022-12-20 | 2023-01-30 | AMD-2024-01-19-call-67.44 | 60.1% | $1102.07 | 11.7% | 5.8% | 40.2% | -34.5% |
| 2023-05-02 | 2023-03-21 | 2023-05-01 | AMD-2024-01-19-call-81.5 | 45.8% | $840.72 | 6.8% | 5.6% | 33.8% | -28.1% |
| 2023-10-31 | 2023-09-19 | 2023-10-30 | AMD-2024-01-19-call-106.06 | 38.5% | $537.67 | 2.0% | 6.6% | 20.8% | -14.2% |
| 2024-01-30 | 2023-12-19 | 2024-01-29 | AMD-2025-01-17-call-123.19 | 32.8% | $1097.50 | 5.8% | 6.9% | 40.2% | -33.4% |

### AMD - pre_earnings_long_call_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 111.8% / 108.6%
Max drawdown: 0.0%
Expectancy: 111.8%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2022-12-20 | 2023-01-30 | AMD-2023-02-03-call-67.44 | 172.3% | $1069.22 | 11.7% | 5.8% | 15.3% | -9.6% |
| 2023-05-02 | 2023-03-21 | 2023-05-01 | AMD-2023-05-05-call-81.5 | 114.7% | $860.10 | 6.8% | 5.6% | 15.3% | -9.7% |
| 2023-10-31 | 2023-09-19 | 2023-10-30 | AMD-2023-11-03-call-106.06 | 57.9% | $564.71 | 2.0% | 6.6% | 15.3% | -8.7% |
| 2024-01-30 | 2023-12-19 | 2024-01-29 | AMD-2024-02-02-call-123.19 | 102.4% | $1160.43 | 5.8% | 6.9% | 15.3% | -8.4% |

### AMD - pre_earnings_long_call_E-20_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 51.5% / 49.4%
Max drawdown: 0.0%
Expectancy: 51.5%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2023-01-03 | 2023-01-30 | AMD-2023-02-03-call-67.44 | 61.6% | $644.16 | 7.2% | 5.8% | 20.5% | -14.7% |
| 2023-05-02 | 2023-04-04 | 2023-05-01 | AMD-2023-05-05-call-81.5 | 30.4% | $374.88 | 2.8% | 5.6% | 20.2% | -14.5% |
| 2023-10-31 | 2023-10-03 | 2023-10-30 | AMD-2023-11-03-call-106.06 | 37.2% | $417.34 | 2.7% | 6.6% | 16.4% | -9.9% |
| 2024-01-30 | 2024-01-02 | 2024-01-29 | AMD-2024-02-02-call-123.19 | 76.8% | $996.02 | 7.1% | 6.9% | 16.4% | -9.5% |

### AMD - earnings_event_long_call

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 27.1% / 26.6%
Max drawdown: 0.0%
Expectancy: 27.1%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2023-01-30 | 2023-02-01 | AMD-2023-02-03-call-67.44 | 17.5% | $321.99 | 0.0% | 5.8% | 29.0% | -23.3% |
| 2023-05-02 | 2023-05-01 | 2023-05-03 | AMD-2023-05-05-call-81.5 | 22.3% | $390.25 | 0.0% | 5.6% | 24.9% | -19.3% |
| 2023-10-31 | 2023-10-30 | 2023-11-01 | AMD-2023-11-03-call-106.06 | 37.9% | $636.02 | 0.0% | 6.6% | 20.5% | -13.9% |
| 2024-01-30 | 2024-01-29 | 2024-01-31 | AMD-2024-02-02-call-123.19 | 30.9% | $770.58 | 0.0% | 6.9% | 24.0% | -17.1% |

### META - long_dated_call_LEAPS_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 49.2% / 48.3%
Max drawdown: 0.0%
Expectancy: 49.2%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2022-12-21 | 2023-01-31 | META-2024-01-19-call-150.67 | 37.4% | $1564.16 | 6.9% | 9.7% | 40.8% | -31.1% |
| 2023-04-26 | 2023-03-15 | 2023-04-25 | META-2024-01-19-call-189.28 | 34.4% | $1527.98 | 5.0% | 9.8% | 34.8% | -24.9% |
| 2023-10-25 | 2023-09-13 | 2023-10-24 | META-2024-01-19-call-260.28 | 59.2% | $2169.23 | 4.9% | 10.9% | 21.8% | -10.9% |
| 2024-02-01 | 2023-12-21 | 2024-01-31 | META-2025-01-17-call-316.48 | 65.9% | $5778.66 | 13.2% | 10.6% | 40.7% | -30.1% |

### META - pre_earnings_long_call_E-30_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 116.1% / 98.6%
Max drawdown: 0.0%
Expectancy: 116.1%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2022-12-21 | 2023-01-31 | META-2023-02-03-call-150.67 | 109.6% | $1612.60 | 6.9% | 9.7% | 15.8% | -6.1% |
| 2023-04-26 | 2023-03-15 | 2023-04-25 | META-2023-04-28-call-189.28 | 87.6% | $1619.69 | 5.0% | 9.8% | 15.8% | -6.0% |
| 2023-10-25 | 2023-09-13 | 2023-10-24 | META-2023-10-27-call-260.28 | 87.0% | $2210.75 | 4.9% | 10.9% | 15.8% | -4.9% |
| 2024-02-01 | 2023-12-21 | 2024-01-31 | META-2024-02-02-call-316.48 | 180.5% | $5550.71 | 13.2% | 10.6% | 15.8% | -5.2% |

### META - pre_earnings_long_call_E-20_to_E-1

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 55.6% / 46.1%
Max drawdown: 0.0%
Expectancy: 55.6%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2023-01-04 | 2023-01-31 | META-2023-02-03-call-150.67 | 28.3% | $680.27 | 2.7% | 9.7% | 20.9% | -11.2% |
| 2023-04-26 | 2023-03-29 | 2023-04-25 | META-2023-04-28-call-189.28 | 23.0% | $648.27 | 1.7% | 9.8% | 20.0% | -10.2% |
| 2023-10-25 | 2023-09-27 | 2023-10-24 | META-2023-10-27-call-260.28 | 63.9% | $1853.86 | 5.8% | 10.9% | 16.9% | -6.0% |
| 2024-02-01 | 2024-01-04 | 2024-01-31 | META-2024-02-02-call-316.48 | 107.3% | $4465.00 | 11.3% | 10.6% | 18.5% | -7.9% |

### META - earnings_event_long_call

Score: 78.00
Samples: 4
Win rate: 100.0%
Mean / median return: 45.5% / 45.5%
Max drawdown: 0.0%
Expectancy: 45.5%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2023-01-31 | 2023-02-02 | META-2023-02-03-call-150.67 | 42.7% | $1433.62 | 0.0% | 9.7% | 25.6% | -15.9% |
| 2023-04-26 | 2023-04-25 | 2023-04-27 | META-2023-04-28-call-189.28 | 48.4% | $1827.53 | 0.0% | 9.8% | 23.8% | -14.0% |
| 2023-10-25 | 2023-10-24 | 2023-10-26 | META-2023-10-27-call-260.28 | 54.6% | $2826.04 | 0.0% | 10.9% | 23.7% | -12.9% |
| 2024-02-01 | 2024-01-31 | 2024-02-02 | META-2024-02-02-call-316.48 | 36.2% | $3397.52 | 0.0% | 10.6% | 30.7% | -20.1% |

### TSLA - long_dated_call_LEAPS_E-30_to_E-1

Score: 72.85
Samples: 4
Win rate: 100.0%
Mean / median return: 17.1% / 17.6%
Max drawdown: 0.0%
Expectancy: 17.1%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2022-12-14 | 2023-01-24 | TSLA-2024-01-19-call-122.3 | 19.6% | $659.53 | 2.9% | -7.5% | 40.7% | -33.2% |
| 2023-04-19 | 2023-03-08 | 2023-04-18 | TSLA-2024-01-19-call-117.04 | 13.4% | $363.52 | 0.9% | -7.5% | 34.7% | -27.2% |
| 2023-10-18 | 2023-09-06 | 2023-10-17 | TSLA-2024-01-19-call-115.24 | 16.0% | $254.40 | -3.7% | -6.7% | 21.7% | -15.0% |
| 2024-01-24 | 2023-12-13 | 2024-01-23 | TSLA-2025-01-17-call-105.89 | 19.3% | $561.03 | 2.9% | -6.5% | 40.7% | -34.2% |

### ORCL - earnings_event_long_call

Score: 72.42
Samples: 4
Win rate: 100.0%
Mean / median return: 16.8% / 15.1%
Max drawdown: 0.0%
Expectancy: 16.8%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-03-08 | 2023-03-10 | ORCL-2023-03-10-call-84.21 | 24.4% | $340.19 | 0.0% | 4.8% | 21.0% | -16.2% |
| 2023-06-12 | 2023-06-09 | 2023-06-13 | ORCL-2023-06-16-call-90.04 | 15.3% | $311.06 | 0.0% | 4.3% | 25.7% | -21.4% |
| 2023-09-11 | 2023-09-08 | 2023-09-12 | ORCL-2023-09-15-call-98.6 | 12.7% | $278.33 | 0.0% | 3.8% | 25.5% | -21.7% |
| 2024-03-11 | 2024-03-08 | 2024-03-12 | ORCL-2024-03-15-call-117.91 | 14.8% | $229.66 | 0.0% | 3.8% | 18.4% | -14.6% |

### ORCL - pre_earnings_long_call_E-20_to_E-1

Score: 72.28
Samples: 4
Win rate: 75.0%
Mean / median return: 40.2% / 44.0%
Max drawdown: -1.8%
Expectancy: 40.2%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-02-09 | 2023-03-08 | ORCL-2023-03-10-call-84.21 | 46.2% | $403.62 | 4.4% | 4.8% | 16.3% | -11.5% |
| 2023-06-12 | 2023-05-15 | 2023-06-09 | ORCL-2023-06-16-call-90.04 | 74.5% | $796.66 | 6.8% | 4.3% | 17.5% | -13.2% |
| 2023-09-11 | 2023-08-14 | 2023-09-08 | ORCL-2023-09-15-call-98.6 | 41.7% | $593.40 | 4.2% | 3.8% | 19.6% | -15.8% |
| 2024-03-11 | 2024-02-12 | 2024-03-08 | ORCL-2024-03-15-call-117.91 | -1.8% | $-26.19 | -2.7% | 3.8% | 17.9% | -14.1% |

### META - pre_earnings_long_call_E-10_to_E-1

Score: 70.40
Samples: 4
Win rate: 100.0%
Mean / median return: 15.7% / 13.9%
Max drawdown: 0.0%
Expectancy: 15.7%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2023-01-18 | 2023-01-31 | META-2023-02-03-call-150.67 | 0.4% | $11.61 | 0.4% | 9.7% | 24.2% | -14.5% |
| 2023-04-26 | 2023-04-12 | 2023-04-25 | META-2023-04-28-call-189.28 | 1.1% | $37.75 | 0.3% | 9.8% | 22.5% | -12.6% |
| 2023-10-25 | 2023-10-11 | 2023-10-24 | META-2023-10-27-call-260.28 | 34.5% | $1218.27 | 4.1% | 10.9% | 18.8% | -7.9% |
| 2024-02-01 | 2024-01-18 | 2024-01-31 | META-2024-02-02-call-316.48 | 26.7% | $1817.40 | 5.3% | 10.6% | 25.0% | -14.4% |

### AMD - pre_earnings_long_call_E-10_to_E-1

Score: 67.45
Samples: 4
Win rate: 75.0%
Mean / median return: 16.9% / 14.1%
Max drawdown: -0.2%
Expectancy: 16.9%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2023-01-17 | 2023-01-30 | AMD-2023-02-03-call-67.44 | 8.0% | $124.86 | 2.0% | 5.8% | 26.2% | -20.4% |
| 2023-05-02 | 2023-04-18 | 2023-05-01 | AMD-2023-05-05-call-81.5 | -0.2% | $-3.06 | 0.2% | 5.6% | 23.7% | -18.1% |
| 2023-10-31 | 2023-10-17 | 2023-10-30 | AMD-2023-11-03-call-106.06 | 20.2% | $258.94 | 2.4% | 6.6% | 17.5% | -11.0% |
| 2024-01-30 | 2024-01-16 | 2024-01-29 | AMD-2024-02-02-call-123.19 | 39.5% | $649.15 | 4.7% | 6.9% | 18.5% | -11.7% |

### TSLA - pre_earnings_long_call_E-20_to_E-1

Score: 66.73
Samples: 4
Win rate: 75.0%
Mean / median return: 17.1% / 11.8%
Max drawdown: -3.1%
Expectancy: 17.1%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2022-12-28 | 2023-01-24 | TSLA-2023-01-27-call-122.3 | 9.4% | $162.91 | -0.2% | -7.5% | 19.4% | -11.9% |
| 2023-04-19 | 2023-03-22 | 2023-04-18 | TSLA-2023-04-21-call-117.04 | -3.1% | $-49.90 | -1.8% | -7.5% | 19.0% | -11.5% |
| 2023-10-18 | 2023-09-20 | 2023-10-17 | TSLA-2023-10-20-call-115.24 | 14.2% | $170.57 | -1.8% | -6.7% | 16.3% | -9.7% |
| 2024-01-24 | 2023-12-27 | 2024-01-23 | TSLA-2024-01-26-call-105.89 | 48.0% | $531.14 | 4.6% | -6.5% | 16.3% | -9.9% |

### ORCL - pre_earnings_long_call_E-10_to_E-1

Score: 55.81
Samples: 4
Win rate: 75.0%
Mean / median return: 10.7% / 9.3%
Max drawdown: -2.5%
Expectancy: 10.7%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-02-23 | 2023-03-08 | ORCL-2023-03-10-call-84.21 | 26.8% | $270.29 | 3.3% | 4.8% | 17.4% | -12.6% |
| 2023-06-12 | 2023-05-29 | 2023-06-09 | ORCL-2023-06-16-call-90.04 | 16.8% | $268.34 | 2.9% | 4.3% | 22.1% | -17.8% |
| 2023-09-11 | 2023-08-28 | 2023-09-08 | ORCL-2023-09-15-call-98.6 | 1.8% | $36.02 | 0.7% | 3.8% | 23.9% | -20.2% |
| 2024-03-11 | 2024-02-26 | 2024-03-08 | ORCL-2024-03-15-call-117.91 | -2.5% | $-36.22 | -1.5% | 3.8% | 17.8% | -14.0% |

### NVDA - pre_earnings_long_call_E-5_to_E-1

Score: 45.13
Samples: 4
Win rate: 75.0%
Mean / median return: 4.8% / 6.4%
Max drawdown: -3.2%
Expectancy: 4.8%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-22 | 2023-02-15 | 2023-02-21 | NVDA-2023-02-24-call-171.38 | 6.6% | $184.51 | 1.6% | 12.7% | 21.0% | -8.3% |
| 2023-05-24 | 2023-05-17 | 2023-05-23 | NVDA-2023-05-26-call-220.65 | 9.6% | $417.32 | 2.5% | 13.1% | 23.6% | -10.5% |
| 2023-08-23 | 2023-08-16 | 2023-08-22 | NVDA-2023-08-25-call-282.01 | 6.1% | $444.67 | 2.5% | 12.9% | 28.0% | -15.1% |
| 2024-02-21 | 2024-02-14 | 2024-02-20 | NVDA-2024-02-23-call-414.48 | -3.2% | $-367.13 | 0.6% | 11.8% | 29.6% | -17.8% |

### AMD - pre_earnings_long_call_E-5_to_E-1

Score: 33.82
Samples: 4
Win rate: 50.0%
Mean / median return: 2.3% / 2.2%
Max drawdown: -8.2%
Expectancy: 2.3%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-31 | 2023-01-24 | 2023-01-30 | AMD-2023-02-03-call-67.44 | -3.0% | $-52.58 | 0.6% | 5.8% | 28.0% | -22.3% |
| 2023-05-02 | 2023-04-25 | 2023-05-01 | AMD-2023-05-05-call-81.5 | -5.4% | $-91.28 | -0.0% | 5.6% | 24.5% | -18.8% |
| 2023-10-31 | 2023-10-24 | 2023-10-30 | AMD-2023-11-03-call-106.06 | 7.4% | $106.56 | 1.4% | 6.6% | 18.6% | -12.1% |
| 2024-01-30 | 2024-01-23 | 2024-01-29 | AMD-2024-02-02-call-123.19 | 10.3% | $215.07 | 2.3% | 6.9% | 21.4% | -14.5% |

### META - pre_earnings_long_call_E-5_to_E-1

Score: 31.90
Samples: 4
Win rate: 50.0%
Mean / median return: 1.3% / 0.2%
Max drawdown: -8.4%
Expectancy: 1.3%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-02-01 | 2023-01-25 | 2023-01-31 | META-2023-02-03-call-150.67 | -4.8% | $-154.81 | 0.1% | 9.7% | 25.0% | -15.3% |
| 2023-04-26 | 2023-04-19 | 2023-04-25 | META-2023-04-28-call-189.28 | -3.8% | $-135.69 | 0.2% | 9.8% | 23.1% | -13.3% |
| 2023-10-25 | 2023-10-18 | 2023-10-24 | META-2023-10-27-call-260.28 | 9.5% | $414.27 | 2.1% | 10.9% | 21.3% | -10.4% |
| 2024-02-01 | 2024-01-25 | 2024-01-31 | META-2024-02-02-call-316.48 | 4.1% | $342.72 | 2.1% | 10.6% | 28.3% | -17.7% |

### TSLA - pre_earnings_long_call_E-10_to_E-1

Score: 27.33
Samples: 4
Win rate: 50.0%
Mean / median return: 1.8% / -3.6%
Max drawdown: -22.1%
Expectancy: 1.8%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2023-01-11 | 2023-01-24 | TSLA-2023-01-27-call-122.3 | -9.7% | $-204.01 | -1.4% | -7.5% | 21.7% | -14.1% |
| 2023-04-19 | 2023-04-05 | 2023-04-18 | TSLA-2023-04-21-call-117.04 | -13.7% | $-247.39 | -1.9% | -7.5% | 20.2% | -12.7% |
| 2023-10-18 | 2023-10-04 | 2023-10-17 | TSLA-2023-10-20-call-115.24 | 2.5% | $33.23 | 0.2% | -6.7% | 17.4% | -10.8% |
| 2024-01-24 | 2024-01-10 | 2024-01-23 | TSLA-2024-01-26-call-105.89 | 28.2% | $359.71 | 3.0% | -6.5% | 17.4% | -11.0% |

### ORCL - pre_earnings_long_call_E-5_to_E-1

Score: 23.31
Samples: 4
Win rate: 25.0%
Mean / median return: -1.0% / -2.9%
Max drawdown: -11.7%
Expectancy: -1.0%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-03-09 | 2023-03-02 | 2023-03-08 | ORCL-2023-03-10-call-84.21 | 8.3% | $97.86 | 1.6% | 4.8% | 19.0% | -14.2% |
| 2023-06-12 | 2023-06-05 | 2023-06-09 | ORCL-2023-06-16-call-90.04 | -0.2% | $-3.33 | 1.1% | 4.3% | 24.4% | -20.1% |
| 2023-09-11 | 2023-09-04 | 2023-09-08 | ORCL-2023-09-15-call-98.6 | -6.2% | $-133.41 | 0.0% | 3.8% | 25.2% | -21.4% |
| 2024-03-11 | 2024-03-04 | 2024-03-08 | ORCL-2024-03-15-call-117.91 | -5.7% | $-86.34 | -0.6% | 3.8% | 18.1% | -14.3% |

### TSLA - pre_earnings_long_call_E-5_to_E-1

Score: 18.80
Samples: 4
Win rate: 25.0%
Mean / median return: -4.6% / -6.7%
Max drawdown: -23.0%
Expectancy: -4.6%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2023-01-18 | 2023-01-24 | TSLA-2023-01-27-call-122.3 | -10.2% | $-215.04 | -0.8% | -7.5% | 21.7% | -14.2% |
| 2023-04-19 | 2023-04-12 | 2023-04-18 | TSLA-2023-04-21-call-117.04 | -11.4% | $-200.28 | -1.0% | -7.5% | 19.8% | -12.3% |
| 2023-10-18 | 2023-10-11 | 2023-10-17 | TSLA-2023-10-20-call-115.24 | -3.2% | $-45.97 | 0.4% | -6.7% | 18.0% | -11.3% |
| 2024-01-24 | 2024-01-17 | 2024-01-23 | TSLA-2024-01-26-call-105.89 | 6.4% | $98.06 | 1.4% | -6.5% | 19.4% | -13.0% |

### TSLA - earnings_event_long_call

Score: 3.00
Samples: 4
Win rate: 0.0%
Mean / median return: -23.3% / -24.6%
Max drawdown: -65.9%
Expectancy: -23.3%

| Event | Entry | Exit | Contract | Return | P&L | Pre-Earnings Drift | Post Move | Implied Move | Realized - Implied |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-01-25 | 2023-01-24 | 2023-01-26 | TSLA-2023-01-27-call-122.3 | -30.2% | $-623.78 | 0.0% | -7.5% | 21.3% | -13.8% |
| 2023-04-19 | 2023-04-18 | 2023-04-20 | TSLA-2023-04-21-call-117.04 | -20.1% | $-339.62 | 0.0% | -7.5% | 19.3% | -11.8% |
| 2023-10-18 | 2023-10-17 | 2023-10-19 | TSLA-2023-10-20-call-115.24 | -13.9% | $-207.94 | 0.0% | -6.7% | 18.5% | -11.8% |
| 2024-01-24 | 2024-01-23 | 2024-01-25 | TSLA-2024-01-26-call-105.89 | -29.1% | $-518.61 | 0.0% | -6.5% | 21.3% | -14.8% |

## Limitations

This report uses fixture data when historical option chains are unavailable. Fixture results test the engine and methodology; they do not establish a live trading edge.
