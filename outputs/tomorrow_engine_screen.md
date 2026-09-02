# Tomorrow Earnings Options Screen

Run context: Wednesday, August 26, 2026  
Target earnings date: Thursday, August 27, 2026  
Purpose: engine-based option screen for earnings-related long-call candidates.

This is not a profitability forecast. The screen uses the engine's contract-selection
and implied-move logic on current option chains where available.

## Filters

- Nearest expiry after the earnings event.
- Near-money calls around 1.02 moneyness, tolerance 0.08.
- Minimum volume: 100.
- Minimum open interest: 250.
- Maximum bid/ask spread: 25%.
- Score rewards lower premium percent, tighter spreads, better liquidity, and lower implied move.

## Ranked Passes

| Rank | Ticker | Timing | Spot | Expiry | Selected Contract | Ask | Premium % | Spread % | Implied Move | Screen Score |
| ---: | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | MRVL | After close | 245.11 | 2026-08-28 | MRVL-2026-08-28-call-250 | 10.65 | 4.34% | 2.38% | 10.33% | 78.06 |
| 2 | IREN | After close | 39.58 | 2026-08-28 | IREN-2026-08-28-call-40.5 | 1.81 | 4.57% | 2.23% | 10.94% | 72.80 |
| 3 | RBRK | After close | 96.13 | 2026-08-28 | RBRK-2026-08-28-call-100 | 4.90 | 5.10% | 10.75% | 12.90% | 52.36 |
| 4 | BBY | Before open | 87.44 | 2026-08-28 | BBY-2026-08-28-call-90 | 2.90 | 3.32% | 20.95% | 8.41% | 51.68 |
| 5 | DLTR | Before open | 132.18 | 2026-08-28 | DLTR-2026-08-28-call-135 | 4.90 | 3.71% | 22.73% | 9.08% | 48.54 |
| 6 | AFRM | After close | 76.46 | 2026-08-28 | AFRM-2026-08-28-call-80 | 2.85 | 3.73% | 23.09% | 10.73% | 40.04 |

## Skipped

| Ticker | Timing | Reason |
| --- | --- | --- |
| WDAY | After close | No liquid near-money call passed filters. |
| ESTC | After close | No liquid near-money call passed filters. |
| ULTA | After close | No liquid near-money call passed filters. |
| DG | Before open | No liquid near-money call passed filters. |
| PD | After close | No liquid near-money call passed filters. |
| S | After close | No liquid near-money call passed filters. |

## Interpretation

MRVL was the cleanest engine pass: tight spread, strong liquidity, premium near 4.3%
of spot, and an implied move around 10.3%. IREN also passed cleanly but is smaller and
likely higher risk. RBRK passed but with a wider spread and higher implied move.

For before-open reporters like BBY and DLTR, buying today would mean holding through an
overnight earnings event. For after-close reporters like MRVL, buying today is earlier
than the event; the engine's conservative pre-earnings rules normally avoid entering on
the announcement session itself unless explicitly using an event-risk setup.
