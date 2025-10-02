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
    Column("start", Time, nullable=True),
    Column("end", Time, nullable=True),
    Column("name", String, nullable=False),
    Column("venue", String, nullable=False),
    Column("link", String, nullable=True),
)

class EventIn(BaseModel):
    date: str       # "YYYY-MM-DD"
    start: Optional[str] = None      # "HH:MM" or None
    end: Optional[str] = None        # "HH:MM" or None
    name: str
    venue: str
    link: Optional[str] = None

class EventOut(BaseModel):
    id: int
    date: str
    start: Optional[str] = None
    end: Optional[str] = None
    name: str
    venue: str
    link: Optional[str] = None