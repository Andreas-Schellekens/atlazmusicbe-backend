from typing import List, Any
from database import fetch_all
from models.event import events

def _format_field(val: Any, time_fmt: str = "%H:%M") -> Any:
    if val is None:
        return None
    # date objects -> ISO date, time objects -> HH:MM, strings left as-is
    try:
        # datetime.date has isoformat, datetime.time has strftime
        if hasattr(val, "isoformat") and not hasattr(val, "strftime"):
            return val.isoformat()
        if hasattr(val, "strftime"):
            return val.strftime(time_fmt)
    except Exception:
        pass
    return val

def get_events() -> List[dict]:
    rows = fetch_all(events)
    out = []
    for r in rows:
        row = dict(r)
        row["date"] = _format_field(row.get("date"))
        row["start"] = _format_field(row.get("start"))
        row["end"] = _format_field(row.get("end"))
        out.append(row)
    return out