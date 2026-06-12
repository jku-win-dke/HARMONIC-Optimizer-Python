from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PopulationBase(ABC, BaseModel):
    population_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
