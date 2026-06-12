from abc import ABC
from typing import Literal

from pydantic import BaseModel


class OrderObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["order"] = "order"
