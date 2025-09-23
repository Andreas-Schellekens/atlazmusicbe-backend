# filepath: c:\Users\Schel\Documents\PersonlijkeProjecten\Atlaz_website\atlazmusicbe-backend\routes\events.py
from fastapi import APIRouter
from typing import List
from queries.event_queries import get_events
from models.event import EventOut

router = APIRouter()

@router.get("/", response_model=List[EventOut])
def list_events():
    return get_events()