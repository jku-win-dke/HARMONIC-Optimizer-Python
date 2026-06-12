from abc import ABC
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.enums.optimization_status import Status


class OptimizationBase(ABC, BaseModel):
    result_size: Optional[int] = None
    
    

class OptimizationCreatedBase(OptimizationBase):
    optimization_id: UUID = None
    status: Status = Status.CREATED
