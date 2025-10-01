from typing import List, Any
from datetime import date, time, datetime as dt
from database import fetch_all
from models.event import events

def _format_field(val: Any, time_fmt: str = "%H:%M") -> Any:
    if val is None:
        return None
    try:
        # explicit type checks to avoid treating date as time
        if isinstance(val, date) and not isinstance(val, dt):
            return val.isoformat()             # date -> "YYYY-MM-DD"
        if isinstance(val, time):
            return val.strftime(time_fmt)     # time -> "HH:MM"
        if isinstance(val, dt):
            return val.isoformat()            # datetime -> ISO
    except Exception:
        pass
    return val

def get_events() -> List[dict]:
    rows = fetch_all(events)
    out: List[dict] = []
    for r in rows:
        row = dict(r)
        row["date"] = _format_field(row.get("date"))
        row["start"] = _format_field(row.get("start"))
        row["end"] = _format_field(row.get("end"))
        out.append(row)
    return out