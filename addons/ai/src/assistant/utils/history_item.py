from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class HistoryItem(Base):
    author = Column(String)
    command = Column(String)
    context_window = Column(Text)
    conversation_id = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow)
    id = Column(Integer, primary_key=True)
    lang = Column(String)
    message = Column(Text)
    model = Column(String)
    personality = Column(String)
    __tablename__ = "assistant_conversation_item"

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)
