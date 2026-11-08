"""Edmonton time, plus the helpers the RA page uses for 'how long has this been open'."""
import os
from datetime import datetime, timedelta, timezone

import pandas as pd

TZ_NAME = "America/Edmonton"  # for reference only. The code below does not look it up.

# Edmonton is UTC-6 for the whole event (Nov 6 to 9, 2026). A fixed offset needs no time zone
# database, so a laptop and the cloud server can never disagree. If it is ever wrong, change
# DEFAULT_OFFSET_HOURS, or set TIME_OFFSET_HOURS in secrets or the environment (for example -7).
DEFAULT_OFFSET_HOURS = -6


def _offset_hours():
    try:
        import streamlit as st

        value = st.secrets["TIME_OFFSET_HOURS"]
    except Exception:
        value = os.environ.get("TIME_OFFSET_HOURS")
    try:
        return float(value)
    except (TypeError, ValueError):
        return DEFAULT_OFFSET_HOURS


LOCAL_TZ = timezone(timedelta(hours=_offset_hours()))

# How long an OPEN report may wait before it is flagged overdue (minutes)
OVERDUE_AFTER_MIN = {"High": 15, "Medium": 120, "Low": 1440}


def now_local():
    """Current time in Edmonton, no matter where the server is."""
    return datetime.now(LOCAL_TZ)


def now_naive():
    return now_local().replace(tzinfo=None)


def _parse_one(value):
    stamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(stamp):
        return pd.NaT
    if stamp.tzinfo is not None:  # saved with a time zone: convert to Edmonton time
        stamp = stamp.tz_convert(LOCAL_TZ).tz_localize(None)
    return stamp


def parse_times(series):
    """Turn saved timestamps into plain Edmonton datetimes, whatever format each was saved in."""
    parsed = [_parse_one(v) for v in series]
    return pd.Series(pd.to_datetime(parsed, errors="coerce"), index=series.index)


def human_age(minutes):
    """90 -> '1 h 30 min'."""
    if pd.isna(minutes) or minutes < 0:
        return "just now"
    minutes = int(minutes)
    if minutes < 1:
        return "under a minute"
    if minutes < 60:
        return f"{minutes} min"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} h {mins} min" if mins else f"{hours} h"
    days, hrs = divmod(hours, 24)
    return f"{days} d {hrs} h" if hrs else f"{days} d"