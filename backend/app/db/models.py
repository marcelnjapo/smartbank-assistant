from sqlalchemy import Column, Integer, String, DateTime, Text

from datetime import datetime

from ..db.database import Base,engine

class TranscriptionHistory(Base):
    __tablename__ = "transcription_history"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String)
    transcript = Column(Text)
    summary = Column(Text)
    sentiment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
Base.metadata.create_all(bind=engine)
