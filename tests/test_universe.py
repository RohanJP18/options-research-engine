from options_research.universe import (
    ListedSymbol,
    dedupe_symbols,
    is_researchable_listing,
    load_public_us_listings,
)


NASDAQ_TEXT = """Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
AAPL|Apple Inc. - Common Stock|Q|N|N|100|N|N
BADW|Example Corp - Warrants|S|N|N|100|N|N
SPY|SPDR S&P 500 ETF Trust|G|N|N|100|Y|N
TEST|Test Corp|G|Y|N|100|N|N
File Creation Time: 0911202600|||||||
"""


OTHER_TEXT = """ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol
BRK.B|Berkshire Hathaway Inc. Class B|N|BRK.B|N|100|N|BRK.B
XYZ.U|Example Acquisition Corp - Units|N|XYZ.U|N|100|N|XYZ.U
File Creation Time: 0911202600|||||||
"""


def test_symbol_universe_removes_junk_listings_and_keeps_common_stocks():
    def http_get(url):
        if url.endswith("nasdaqlisted.txt"):
            return NASDAQ_TEXT
        return OTHER_TEXT

    listings = load_public_us_listings(http_get)

    assert [listing.yahoo_symbol for listing in listings] == ["AAPL", "BRK-B"]


def test_etfs_are_optional_in_the_universe():
    spy = ListedSymbol("SPY", "SPDR S&P 500 ETF Trust", "NASDAQ", is_etf=True)

    assert not is_researchable_listing(spy)
    assert is_researchable_listing(spy, include_etfs=True)


def test_dedupe_symbols_uses_yahoo_symbol_form():
    listings = [
        ListedSymbol("BRK.B", "Berkshire Hathaway Inc.", "NYSE"),
        ListedSymbol("BRK-B", "Berkshire Hathaway Inc.", "NYSE"),
    ]

    assert [listing.yahoo_symbol for listing in dedupe_symbols(listings)] == ["BRK-B"]
