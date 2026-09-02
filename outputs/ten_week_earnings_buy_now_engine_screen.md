# Ten-Week Earnings Buy-Now Engine Screen

Run context: Wednesday, August 26, 2026  
Target window: earnings after August 26 through November 4, 2026  
Bucket: buy now, hold toward a future earnings event, selected call expiry after earnings.

The engine screened a liquid-options universe and applied these filters:

- Upcoming earnings inside the next 10 weeks.
- Near-money call around 1.03 moneyness.
- Expiry after the earnings date.
- Minimum volume: 100.
- Minimum open interest: 250.
- Maximum spread: 25%.
- Score rewards lower premium, tighter spread, stronger liquidity, stronger momentum,
  lower implied move, and enough time before the event.

## Strong Passes

Strong means score >= 70.

| Rank | Ticker | Event | Days Away | Expiry | Contract | Ask | Premium % | Spread % | Implied Move | 5D | 20D | 60D | Score |
| ---: | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | BAC | 2026-10-14 | 49 | 2026-10-16 | BAC-2026-10-16-call-65 | 1.09 | 1.75% | 4.69% | 7.17% | -1.49% | 1.90% | 21.44% | 83.1 |
| 2 | SLB | 2026-10-23 | 58 | 2026-11-20 | SLB-2026-11-20-call-57.5 | 2.33 | 4.35% | 5.29% | 13.56% | 0.09% | 9.48% | -1.59% | 75.2 |
| 3 | AMZN | 2026-10-29 | 64 | 2026-11-20 | AMZN-2026-11-20-call-270 | 14.65 | 5.63% | 2.42% | 13.52% | -2.09% | 14.84% | -0.38% | 73.1 |
| 4 | PFE | 2026-11-03 | 69 | 2026-11-20 | PFE-2026-11-20-call-29 | 1.13 | 3.99% | 8.29% | 9.89% | 0.21% | 12.52% | 12.35% | 71.4 |
| 5 | NFLX | 2026-10-20 | 55 | 2026-11-20 | NFLX-2026-11-20-call-85 | 5.00 | 6.14% | 3.05% | 15.01% | 1.55% | 10.63% | -5.11% | 70.7 |
| 6 | C | 2026-10-13 | 48 | 2026-10-16 | C-2026-10-16-call-140 | 3.60 | 2.70% | 7.19% | 8.78% | 0.50% | 5.59% | 3.99% | 70.2 |

## Near Misses

| Ticker | Event | Contract | Score | Note |
| --- | --- | --- | ---: | --- |
| TSM | 2026-10-15 | TSM-2026-10-16-call-440 | 68.5 | Good, just below strong threshold. |
| MSFT | 2026-10-28 | MSFT-2026-11-20-call-510 | 67.4 | Quality name, score held down by premium/liquidity mix. |
| MRVL | 2026-08-27 | MRVL-2026-09-04-call-252.5 | 63.3 | Too close to event for buy-now pre-earnings bucket. |
| HPE | 2026-09-02 | HPE-2026-09-04-call-57 | 60.0 | Momentum strong, but score still below 70. |

## Interpretation

The engine did find strong earnings-bucket candidates over the full 10-week window.
However, the strongest names were not the obvious next-week AI/semiconductor trades.

- BAC and C scored well because the contracts were cheap, liquid, and the implied moves were modest.
- AMZN scored well because the spread was tight and 20-day momentum was strong.
- NFLX barely cleared the strong threshold; its 60-day momentum was weaker.
- The next-week AI names, including AVGO and HPE, did not clear the strong threshold.

This screen should be treated as a research shortlist, not a guarantee or recommendation.
