from abc import ABC
from typing import Literal

from pydantic import BaseModel, model_validator


class QuantilesObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["quantiles"] = "quantiles"
    quantiles: int

    @model_validator(mode='after')
    def check_top(self):
        if self.quantiles < 2:
            raise ValueError('Number of quantiles must be greater than or equal to 2')
        return self