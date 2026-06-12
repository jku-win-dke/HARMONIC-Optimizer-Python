from abc import ABC

from pydantic import BaseModel


class ObjectiveWeightBase(ABC, BaseModel):
    objective_id: str
    weight: float
