from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, Date, Time
from database import metadata

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("start", Time, nullable=False),
    Column("end", Time, nullable=False),
    Column("name", String, nullable=False),
    Column("venue", String, nullable=False),
    Column("link", String, nullable=True),
)

class EventIn(BaseModel):
    date: str       # "YYYY-MM-DD"
    start: str      # "HH:MM"
    end: str        # "HH:MM"
    name: str
    venue: str
    link: Optional[str] = None

class EventOut(EventIn):
    id: int