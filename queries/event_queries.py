from typing import List, Any, Optional, Dict
from datetime import date, time, datetime as dt
from sqlalchemy import insert, update, delete, select
from database import fetch_all, fetch_one_by_id, execute_returning
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

def _format_row(raw: Dict[str, Any]) -> Dict[str, Any]:
    row = dict(raw)
    row["date"] = _format_field(row.get("date"))
    row["start"] = _format_field(row.get("start"))
    row["end"] = _format_field(row.get("end"))
    return row

def get_events() -> List[dict]:
    rows = fetch_all(events)
    return [_format_row(r) for r in rows]

def get_event(event_id: int) -> Optional[dict]:
    row = fetch_one_by_id(events, event_id)
    return _format_row(row) if row else None

def create_event(data: Dict[str, Any]) -> dict:
    stmt = insert(events).values(
        date=data.get("date"),
        start=data.get("start"),
        end=data.get("end"),
        name=data.get("name"),
        venue=data.get("venue"),
        link=data.get("link"),
    ).returning(events)
    returned = execute_returning(stmt)
    if returned:
        return _format_row(returned[0])
    raise RuntimeError("Failed to create event")

def update_event(event_id: int, data: Dict[str, Any]) -> Optional[dict]:
    stmt = update(events).where(events.c.id == event_id).values(
        date=data.get("date"),
        start=data.get("start"),
        end=data.get("end"),
        name=data.get("name"),
        venue=data.get("venue"),
        link=data.get("link"),
    ).returning(events)
    returned = execute_returning(stmt)
    return _format_row(returned[0]) if returned else None

def delete_event(event_id: int) -> bool:
    stmt = delete(events).where(events.c.id == event_id).returning(events.c.id)
    returned = execute_returning(stmt)
    return bool(returned)