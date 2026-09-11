# Broad Market Live Options Scan - 2026-09-11

This is a live research snapshot, not a trade recommendation or guarantee. Prices and
option quotes were current around 2026-09-11 09:20 Pacific and will move.

## Data Sources

- Public U.S. listing universe: Nasdaq Trader listed-symbol directories.
- Broad live options-activity screen: Robinhood scanner market data.
- Contract quotes and Greeks: Robinhood option quote data.
- Selected underlying price history for score components: Yahoo Finance daily history.

## Broad Discovery Pass

The public-listing loader found 5,247 U.S. listings after listing-type cleanup. The
Yahoo price-history pass narrowed that to 1,814 liquid underlyings, but the all-chain
Yahoo option crawl was rate-limited before completion.

To finish the broad market discovery without pretending the Yahoo crawl completed, the
live scanner was run across public U.S. stocks with these filters:

- Stock only.
- Price at least $5.
- Market cap at least $1B.
- 30-day average share volume at least 500k.
- Same-day call volume at least 2,000.
- Aggregate call open interest at least 25,000.
- Same-day call premium traded at least $1M.
- 5-day momentum positive.
- 90-day ATM IV no more than 1.35x 1-month realized volatility.

That broad pass returned 79 matching stocks.

## Contract-Level Results

Normal engine contract constraints were then applied to representative earnings/pre-
earnings calls from the strongest broad-scan names:

- Max contract cost: $3,000.
- Min option volume: 50.
- Min open interest: 250.
- Min premium-dollar volume: $25,000.
- Max bid/ask spread: 25%.
- DTE: 14 to 760.
- Call moneyness: 0.85x to 1.25x underlying price.

| Ticker | Contract | Score | Ask | Cost | Bid/Ask | Vol/OI | IV | Breakeven Need | Read |
| --- | --- | ---: | ---: | ---: | --- | --- | ---: | ---: | --- |
| AAPL | 2026-11-20 $360 call | 86.7 | $7.00 | $700 | $6.85/$7.00 | 955/12,438 | 26.2% | 9.8% | Best clean pass: huge call-dollar flow, tight spread, solid 5/20/60-day trend, and IV close to recent realized volatility. |
| AMD | 2026-11-20 $600 call | 75.5 | $23.95 | $2,395 | $22.85/$23.95 | 1,561/2,777 | 56.6% | 21.5% | Passed, but less clean: very strong 5-day move and massive call flow, but the breakeven is demanding. |

## Near Misses And Rejects

| Ticker | Contract Checked | Engine Result | Why |
| --- | --- | ---: | --- |
| META | 2026-11-20 $750 call | 71.9 | Great stock-level setup, but the contract fit was weak because breakeven required an 18% move. |
| CVX | 2026-11-20 $230 call | 67.2 | Tight enough contract, but IV was expensive versus recent realized movement and liquidity score was only moderate. |
| HPE | 2026-12-18 $70 call | 65.4 | Momentum strong, but spread was wide and breakeven required roughly 24%. |
| INTC | 2026-11-20 $115 call | 65.4 | Good liquidity, but 20/60-day trend was weak and breakeven required roughly 19%. |
| BE | 2026-11-20 $320 call | 64.1 | Strong momentum, but expensive contract fit and high volatility made it less clean. |
| ANET | 2026-11-20 $220 call | 63.0 | Acceptable contract, but liquidity score and 20-day trend were not strong enough. |
| AVGO | 2026-12-18 $400 call | 59.0 | Tight/liquid option, but recent 20/60-day trend was weak in the scoring model. |
| CSCO | 2026-11-20 $120 call | 56.4 | Cheap and tight, but weak medium-term trend and IV value hurt the score. |
| ALAB | 2026-11-20 $330 call | 44.4 | Contract was almost at the $3k cap and medium-term trend was poor. |
| XOM | 2026-11-20 $180 call | Filtered | Failed minimum option volume. |
| SWKS | 2026-11-20 $100 call | Filtered | Failed minimum option volume and premium-dollar volume. |
| GLW | 2026-11-20 $180 call | Filtered | Failed minimum option volume and premium-dollar volume. |
| MRVL | 2026-12-18 $270 call | Filtered | Failed minimum option volume. |
| COHR | 2026-11-20 $350 call | Filtered | Failed minimum option volume and open interest. |
| HPQ | 2026-12-18 $40 call | Filtered | Failed max spread rule. |
| DELL | 2026-12-18 $650/$700 calls | Filtered | Underlying setup was strong, but reasonable contracts exceeded the $3k cost cap. |

## Bottom Line

Using the strict engine rules, only two checked contracts from the market-wide discovery
pass cleared 75 today: AAPL and AMD. AAPL was the only truly clean high-score result.
AMD passed, but it is a higher-risk, higher-breakeven setup. The scan did not justify
forcing four or five buys just to fill a list.
