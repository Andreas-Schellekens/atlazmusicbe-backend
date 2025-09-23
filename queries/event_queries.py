from typing import List
from database import fetch_all
from models.event import events

def get_events() -> List[dict]:
    rows = fetch_all(events)
    out = []
    for r in rows:
        row = dict(r)
        # format date/time to the exact string shapes you requested
        if row.get("date") is not None:
            row["date"] = row["date"].isoformat()  # "YYYY-MM-DD"
        if row.get("start") is not None:
            row["start"] = row["start"].strftime("%H:%M")  # "HH:MM"
        if row.get("end") is not None:
            row["end"] = row["end"].strftime("%H:%M")    # "HH:MM"
        out.append(row)
    return out