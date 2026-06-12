from abc import ABC
from typing import Literal

from pydantic import BaseModel


class ObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["order", "top", "above", "order_quantiles", "fitness_range"]
