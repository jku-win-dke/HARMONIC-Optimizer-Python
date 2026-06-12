from abc import ABC
from typing import Literal

from pydantic import BaseModel


class AboveObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["above"] = "above"
    threshold: int
