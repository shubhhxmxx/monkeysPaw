from pydantic import BaseModel
from datetime import datetime

class WishRequest(BaseModel):
    wish: str

class WishResponse(BaseModel):
    wish: str
    twist: str
    id: int
    timestamp: datetime