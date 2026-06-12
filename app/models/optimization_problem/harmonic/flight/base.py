from abc import ABC
from datetime import datetime

from pydantic import BaseModel


class FlightBase(ABC, BaseModel):
    flight_id: str
    scheduled_time: datetime
