from abc import ABC
from datetime import datetime

from pydantic import BaseModel


class TargetTimeBase(ABC, BaseModel):
    target_time_id: str
    time: datetime
