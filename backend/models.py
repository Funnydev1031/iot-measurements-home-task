from typing import Optional
from pydantic import BaseModel

class Location(BaseModel):
    id: int
    name: str

class Device(BaseModel):
    id: int
    location_id: int
    mac: str

class Metric(BaseModel):
    id: int
    name: str
    unit: Optional[str] = None