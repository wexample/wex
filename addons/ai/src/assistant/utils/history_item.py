from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HistoryItem(Base):
    __tablename__ = 'assistant_conversation_item'
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer)
    message = Column(String)
    date_created = Column(DateTime)

    def __init__(self, **kw: Any) -> None:
        super().__init__(**kw)

        self.date_created = datetime.now()
