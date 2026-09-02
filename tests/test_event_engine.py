from datetime import date

import pandas as pd

from options_research.events import EventEngine
from options_research.models import EarningsEvent


def test_postmarket_event_alignment_and_pre_earnings_windows():
    sessions = pd.bdate_range("2024-02-12", "2024-02-26")
    prices = pd.DataFrame(
        {"ticker": "XYZ", "date": sessions.date, "close": range(100, 100 + len(sessions))}
    )

    engine = EventEngine(prices)
    event = EarningsEvent("XYZ", date(2024, 2, 21), "postmarket")

    aligned = engine.align_event(event)

    assert aligned.announcement_session == date(2024, 2, 21)
    assert aligned.last_pre_event_session == date(2024, 2, 20)
    assert aligned.first_post_event_session == date(2024, 2, 22)
    assert engine.pre_event_window(event, 5) == (date(2024, 2, 14), date(2024, 2, 20))


def test_premarket_event_alignment_uses_same_day_as_post_event_session():
    sessions = pd.bdate_range("2024-04-22", "2024-05-03")
    prices = pd.DataFrame(
        {"ticker": "XYZ", "date": sessions.date, "close": range(50, 50 + len(sessions))}
    )

    engine = EventEngine(prices)
    event = EarningsEvent("XYZ", date(2024, 4, 30), "premarket")

    aligned = engine.align_event(event)

    assert aligned.last_pre_event_session == date(2024, 4, 29)
    assert aligned.first_post_event_session == date(2024, 4, 30)


def test_no_future_leakage_requires_known_event_and_quote_dates_before_entry():
    sessions = pd.bdate_range("2024-02-01", "2024-02-29")
    prices = pd.DataFrame(
        {"ticker": "XYZ", "date": sessions.date, "close": range(100, 100 + len(sessions))}
    )
    engine = EventEngine(prices)
    event = EarningsEvent(
        "XYZ",
        date(2024, 2, 21),
        "postmarket",
        announced_on=date(2024, 2, 1),
    )

    entry, _ = engine.pre_event_window(event, 5)

    assert engine.event_is_known_by(event, entry)
    assert engine.quote_is_eligible(date(2024, 2, 14), entry)
    assert not engine.quote_is_eligible(date(2024, 2, 22), entry)
    assert not engine.event_is_known_by(
        EarningsEvent("XYZ", date(2024, 2, 21), "postmarket", announced_on=date(2024, 2, 16)),
        entry,
    )
