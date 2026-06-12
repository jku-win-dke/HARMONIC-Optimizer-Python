from abc import ABC
from typing import Literal

from pydantic import BaseModel


class OptimizationFrameworkBase(ABC, BaseModel):
    framework_type: Literal["scipy", "pygad"]
