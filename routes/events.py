# filepath: c:\Users\Schel\Documents\PersonlijkeProjecten\Atlaz_website\atlazmusicbe-backend\routes\events.py
from fastapi import APIRouter, HTTPException
from typing import List
from queries.event_queries import (
    get_events,
    get_event,
    create_event,
    update_event,
    delete_event,
)
from models.event import EventOut, EventIn

router = APIRouter()

@router.get("/", response_model=List[EventOut])
def list_events():
    try:
        return get_events()
    except Exception as exc:
        # surface DB/formatting errors as a 503 so logs show the root cause
        raise HTTPException(status_code=503, detail=str(exc))

@router.post("/", response_model=EventOut, status_code=201)
def create(event_in: EventIn):
    try:
        created = create_event(event_in.dict())
        return created
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))

@router.get("/{event_id}", response_model=EventOut)
def read(event_id: int):
    ev = get_event(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return ev

@router.put("/{event_id}", response_model=EventOut)
def replace(event_id: int, event_in: EventIn):
    updated = update_event(event_id, event_in.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated

@router.delete("/{event_id}", status_code=204)
def remove(event_id: int):
    ok = delete_event(event_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Event not found")
    return None