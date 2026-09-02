from __future__ import annotations

from datetime import date
from typing import List, Optional, Tuple

import pandas as pd

from .models import AlignedEvent, EarningsEvent


class EventEngine:
    """Aligns earnings events to tradable sessions using only data known at entry."""

    def __init__(self, prices: pd.DataFrame):
        if prices.empty:
            raise ValueError("prices must not be empty")
        self.prices = prices.copy()
        self.prices["date"] = pd.to_datetime(self.prices["date"]).dt.date

    def sessions(self, ticker: Optional[str] = None) -> List[date]:
        data = self.prices
        if ticker is not None:
            data = data[data["ticker"] == ticker]
        return sorted(data["date"].unique())

    def price_on(self, ticker: str, session: date, field: str = "close") -> float:
        rows = self.prices[(self.prices["ticker"] == ticker) & (self.prices["date"] == session)]
        if rows.empty:
            raise KeyError(f"no price for {ticker} on {session}")
        return float(rows.iloc[0][field])

    def session_on_or_before(self, target: date, ticker: Optional[str] = None) -> date:
        candidates = [session for session in self.sessions(ticker) if session <= target]
        if not candidates:
            raise ValueError(f"no trading session on or before {target}")
        return candidates[-1]

    def session_on_or_after(self, target: date, ticker: Optional[str] = None) -> date:
        candidates = [session for session in self.sessions(ticker) if session >= target]
        if not candidates:
            raise ValueError(f"no trading session on or after {target}")
        return candidates[0]

    def trading_day_offset(
        self, anchor: date, offset: int, ticker: Optional[str] = None
    ) -> date:
        sessions = self.sessions(ticker)
        if anchor not in sessions:
            anchor = self.session_on_or_before(anchor, ticker)
        index = sessions.index(anchor) + offset
        if index < 0 or index >= len(sessions):
            raise ValueError(f"offset {offset} from {anchor} is outside available data")
        return sessions[index]

    def align_event(self, event: EarningsEvent) -> AlignedEvent:
        announcement_session = self.session_on_or_before(event.event_date, event.ticker)
        timing = event.timing.lower()
        if timing == "premarket":
            first_post = self.session_on_or_after(event.event_date, event.ticker)
        elif timing == "postmarket":
            first_post = self.trading_day_offset(announcement_session, 1, event.ticker)
        else:
            raise ValueError(f"unsupported earnings timing: {event.timing}")
        last_pre = self.trading_day_offset(announcement_session, -1, event.ticker)
        return AlignedEvent(
            event=event,
            announcement_session=announcement_session,
            last_pre_event_session=last_pre,
            first_post_event_session=first_post,
        )

    def pre_event_window(self, event: EarningsEvent, days: int) -> Tuple[date, date]:
        if days < 1:
            raise ValueError("days must be >= 1")
        aligned = self.align_event(event)
        entry = self.trading_day_offset(aligned.last_pre_event_session, -(days - 1), event.ticker)
        return entry, aligned.last_pre_event_session

    @staticmethod
    def quote_is_eligible(quote_date: date, entry_date: date) -> bool:
        return quote_date <= entry_date

    @staticmethod
    def event_is_known_by(event: EarningsEvent, entry_date: date) -> bool:
        return event.announced_on is None or event.announced_on <= entry_date
