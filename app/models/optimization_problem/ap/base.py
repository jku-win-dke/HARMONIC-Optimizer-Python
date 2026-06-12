from abc import ABC
from typing import Literal

from pydantic import BaseModel


class AssignmentProblemBase(ABC, BaseModel):
    problem_type: Literal["ap"] = "ap"
