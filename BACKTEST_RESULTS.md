# Backtest Results

Run date: 2026-08-26  
Command:

```bash
python3 -m options_research.cli \
  --tickers NVDA TSLA ORCL AMD META \
  --start 2023-01-01 \
  --end 2024-12-31 \
  --output outputs/options_research_report.md
```

Test command:

```bash
python3 -m pytest -q
```

Verified test result: `11 passed`.

## Data Used

The run used deterministic fixture data for NVDA, TSLA, ORCL, AMD, and META. The fixture
contains synthetic underlying prices, known earnings dates, and synthetic option chains
with bid/ask spreads, deltas, volume, and open interest.

This is a methodology and software-validation backtest. It is not evidence of a live
trading edge because it does not use real historical option-chain data.

## Aggregate Fixture Results

| Strategy | Completed Samples | Average Win Rate | Average Mean Return |
| --- | ---: | ---: | ---: |
| `long_dated_call_LEAPS_E-30_to_E-1` | 20 | 100.0% | 42.2% |
| `pre_earnings_long_call_E-30_to_E-1` | 20 | 100.0% | 101.2% |
| `pre_earnings_long_call_E-20_to_E-1` | 20 | 90.0% | 48.7% |
| `pre_earnings_long_call_E-10_to_E-1` | 20 | 80.0% | 14.0% |
| `pre_earnings_long_call_E-5_to_E-1` | 20 | 45.0% | 0.6% |
| `earnings_event_long_call` | 20 | 80.0% | 23.8% |

## Top Ranked Fixture Cases

Several NVDA, AMD, META, and ORCL pre-earnings windows ranked highly, especially the
E-30 and E-20 windows. TSLA earnings-event long calls ranked poorly in the fixture run,
with a 0.0% win rate and a -23.3% mean option return.

The full per-trade report is in `outputs/options_research_report.md`.

## Edge Assessment

| Strategy Family | Fixture Observation | Evidence Of Real Edge? |
| --- | --- | --- |
| Long-dated calls / LEAPS | Positive fixture returns across all five tickers. | No. Needs real chains and larger samples. |
| Pre-earnings long calls | Longer windows performed better than E-5 in the fixture. | No. Synthetic drift was intentionally present in fixtures. |
| Earnings-event long calls | Mixed by ticker; TSLA was strongly negative in the fixture. | No. Event exposure needs real IV crush and chain data. |

## Limitations

- Historical option-chain data was not available in this environment.
- Fixture option prices are synthetic and deterministic.
- Sample sizes are intentionally small: four events per ticker, twenty cases per strategy row.
- The opportunity score is useful for sorting research candidates, not for trading decisions.
- Real deployment needs survivorship-bias-aware symbols, corporate action handling,
  real earnings announcement timestamps, real bid/ask chains, commissions, assignment
  rules, and broker-specific execution assumptions.

## Conclusion

The engine is runnable end to end and the methodology checks are covered by tests. The
fixture backtest does not prove profitability. The next meaningful step is adding a
licensed historical option-chain data adapter and re-running the same strategies without
changing the research logic.
