from abc import ABC
from typing import List

from pydantic import BaseModel


class AssignmentBase(ABC, BaseModel):
    row_ind: List[int]
    col_ind: List[int]