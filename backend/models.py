# backend/models.py
from pydantic import BaseModel
from typing import Optional, List

class DvrCredentials(BaseModel):
    ip: str
    username: str
    password: str

class AlertData(BaseModel):
    camera_id: str
    timestamp: str
    alert_type: str
    confidence: float
    image_data: Optional[str] = None
    metadata: Optional[dict] = None