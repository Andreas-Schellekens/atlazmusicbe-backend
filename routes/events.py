# filepath: c:\Users\Schel\Documents\PersonlijkeProjecten\Atlaz_website\atlazmusicbe-backend\routes\events.py
from fastapi import APIRouter, HTTPException
from typing import List
from queries.event_queries import get_events
from models.event import EventOut

router = APIRouter()

@router.get("/", response_model=List[EventOut])
def list_events():
    try:
        return get_events()
    except Exception as exc:
        # surface DB/formatting errors as a 503 so logs show the root cause
        raise HTTPException(status_code=503, detail=str(exc))