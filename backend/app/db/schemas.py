from pydantic import BaseModel
from datetime import datetime

class TranscriptionHistoryCreate(BaseModel):
    username: str
    email: str
    role: str
    transcript: str
    summary: str
    sentiment: str

class TranscriptionHistoryResponse(TranscriptionHistoryCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
