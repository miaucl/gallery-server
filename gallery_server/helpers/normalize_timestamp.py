"""Helper functions."""

from datetime import datetime, timedelta


def normalize_timestamp(granularity: str) -> datetime:
    """Normalize the current timestamp to the specified granularity.

    Parameters
    ----------
    granularity
        Granularity level ("year", "month", "week", "day", "hour", "minute", "second")

    Returns
    -------
    datetime
        A datetime object normalized to the specified granularity.

    """
    now = datetime.now()

    granularity_map = {
        "year": datetime(now.year, 1, 1),
        "month": datetime(now.year, now.month, 1),
        "week": datetime(now.year, now.month, now.day) - timedelta(days=now.weekday()),
        "day": datetime(now.year, now.month, now.day),
        "hour": datetime(now.year, now.month, now.day, now.hour),
        "minute": datetime(now.year, now.month, now.day, now.hour, now.minute),
        "second": datetime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        ),
    }

    return granularity_map.get(granularity, now)
