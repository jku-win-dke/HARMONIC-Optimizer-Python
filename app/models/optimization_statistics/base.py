from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StatisticsBase(ABC, BaseModel):
    time_optimization_created: Optional[datetime] = None
