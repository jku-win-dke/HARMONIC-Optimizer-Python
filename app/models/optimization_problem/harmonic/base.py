from abc import ABC
from typing import Literal

from pydantic import BaseModel


class HarmonicProblemBase(ABC, BaseModel):
    problem_type: Literal["harmonic"] = "harmonic"
