from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Callable, Iterable, List

import pandas as pd


NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"


@dataclass(frozen=True)
class ListedSymbol:
    symbol: str
    name: str
    exchange: str
    is_etf: bool = False

    @property
    def yahoo_symbol(self) -> str:
        return self.symbol.replace(".", "-").strip()


EXCLUDED_NAME_TERMS = (
    " warrant",
    " warrants",
    " unit",
    " units",
    " right",
    " rights",
    " preferred",
    " preference",
    " notes",
    " note ",
    " bond",
    " debenture",
    " etn",
    " fund",
    " trust",
    " acquisition corp",
)


def parse_nasdaq_listed(text: str) -> List[ListedSymbol]:
    data = pd.read_csv(StringIO(text), sep="|")
    data = data[data["Symbol"].astype(str) != "File Creation Time"]
    records: List[ListedSymbol] = []
    for _, row in data.iterrows():
        if str(row["Test Issue"]).strip().upper() == "Y":
            continue
        records.append(
            ListedSymbol(
                symbol=str(row["Symbol"]).strip(),
                name=str(row["Security Name"]).strip(),
                exchange="NASDAQ",
                is_etf=str(row["ETF"]).strip().upper() == "Y",
            )
        )
    return records


def parse_other_listed(text: str) -> List[ListedSymbol]:
    data = pd.read_csv(StringIO(text), sep="|")
    data = data[data["ACT Symbol"].astype(str) != "File Creation Time"]
    records: List[ListedSymbol] = []
    for _, row in data.iterrows():
        if str(row["Test Issue"]).strip().upper() == "Y":
            continue
        records.append(
            ListedSymbol(
                symbol=str(row["ACT Symbol"]).strip(),
                name=str(row["Security Name"]).strip(),
                exchange=str(row["Exchange"]).strip(),
                is_etf=str(row["ETF"]).strip().upper() == "Y",
            )
        )
    return records


def is_researchable_listing(listing: ListedSymbol, include_etfs: bool = False) -> bool:
    symbol = listing.yahoo_symbol
    name = f" {listing.name.lower()} "
    if not symbol or "^" in symbol or " " in symbol or "$" in symbol:
        return False
    if listing.is_etf:
        return include_etfs
    return not any(term in name for term in EXCLUDED_NAME_TERMS)


def dedupe_symbols(listings: Iterable[ListedSymbol]) -> List[ListedSymbol]:
    seen = set()
    deduped: List[ListedSymbol] = []
    for listing in listings:
        symbol = listing.yahoo_symbol
        if symbol in seen:
            continue
        seen.add(symbol)
        deduped.append(listing)
    return deduped


def load_public_us_listings(
    http_get: Callable[[str], str],
    include_etfs: bool = False,
) -> List[ListedSymbol]:
    listings = parse_nasdaq_listed(http_get(NASDAQ_LISTED_URL))
    listings.extend(parse_other_listed(http_get(OTHER_LISTED_URL)))
    return [
        listing
        for listing in dedupe_symbols(listings)
        if is_researchable_listing(listing, include_etfs=include_etfs)
    ]
