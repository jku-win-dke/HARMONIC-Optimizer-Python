from abc import ABC
from typing import Optional

from pydantic import BaseModel


class FitnessBase(ABC, BaseModel):
    objective_id: str
    actual_fitness: Optional[int] = None
    estimated_fitness: Optional[int] = None
