# Next Week Earnings Buy-Now Screen

Run context: Wednesday, August 26, 2026  
Target window: earnings from Tuesday, September 1 through Friday, September 4, 2026  
Purpose: screen candidates that could be bought now ahead of next week's earnings.

This is an engine screen, not a recommendation or a promise of profitability. It uses
current option-chain data where available and applies the project's contract-selection
rules: near-money calls, expiry after event, minimum liquidity, and maximum spread.

## Ranked Passes

| Rank | Ticker | Event Date | Expiry | Spot | Selected Contract | Ask | Premium % | Spread % | Volume | Open Interest | Implied Move | 5D Return | 20D Return | Score |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | NIO | 2026-09-01 | 2026-09-04 | 4.37 | NIO-2026-09-04-call-4.5 | 0.16 | 3.66% | 6.45% | 3408 | 5193 | 9.38% | -4.59% | -8.19% | 64.37 |
| 2 | HPE | 2026-09-02 | 2026-09-04 | 55.23 | HPE-2026-09-04-call-57 | 2.86 | 5.18% | 5.76% | 176 | 552 | 12.72% | 3.95% | 24.28% | 54.18 |
| 3 | AVGO | 2026-09-02 | 2026-09-04 | 355.59 | AVGO-2026-09-04-call-365 | 13.25 | 3.73% | 9.90% | 232 | 526 | 8.75% | -1.90% | -3.98% | 48.84 |

## Skipped

| Ticker | Event Date | Reason |
| --- | --- | --- |
| LULU | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| DOCU | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| ZS | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| CIEN | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| MDB | 2026-09-01 | No near-money call passed liquidity/spread filters. |
| GTLB | 2026-09-01 | No near-money call passed liquidity/spread filters. |
| ASAN | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| AI | 2026-09-02 | No near-money call passed liquidity/spread filters. |
| PATH | 2026-09-03 | No near-money call passed liquidity/spread filters. |
| CRDO | 2026-09-01 | No near-money call passed liquidity/spread filters. |
| CPB | 2026-09-03 | No near-money call passed liquidity/spread filters. |

## Interpretation

NIO ranked first because its call was cheap, liquid, and not too wide, but its 5-day and
20-day price momentum were both negative. HPE had the strongest recent momentum but a
larger premium and a larger implied move. AVGO had the best thematic fit to the AI-chip
idea and a reasonable premium, but weaker recent momentum and a wider spread than the top
ranked name.

Engine-only shortlist: NIO, HPE, AVGO. Quality-adjusted shortlist: AVGO and HPE.
