from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HistoryItem(Base):
    __tablename__ = 'assistant_conversation_item'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime)
    author = Column(String)
    context_window = Column(Text)
    message = Column(Text)
    model = Column(String)
    lang = Column(String)
    conversation_id = Column(Integer)
    personality = Column(String)
    command = Column(String)

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)

        self.date_created = datetime.now()
