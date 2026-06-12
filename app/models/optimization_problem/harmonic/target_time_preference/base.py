from abc import ABC
from typing import List

from pydantic import BaseModel


class TargetTimePreferenceBase(ABC, BaseModel):
    weight: int | List[str]
