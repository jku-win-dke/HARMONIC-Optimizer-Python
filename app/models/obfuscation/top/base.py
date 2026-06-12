from abc import ABC
from typing import Literal

from pydantic import BaseModel, model_validator


class TopObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["top"] = "top"
    top: int

    @model_validator(mode='after')
    def check_top(self):
        if self.top < 3:
            raise ValueError('Top must be greater than or equal to 3')
        return self