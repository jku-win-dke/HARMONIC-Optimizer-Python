from abc import ABC
from typing import Literal

from pydantic import BaseModel


class OptimizationProblemBase(ABC, BaseModel):
    problem_type: Literal["harmonic", "ap"]
