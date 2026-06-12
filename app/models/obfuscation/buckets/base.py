from abc import ABC
from typing import Literal

from pydantic import BaseModel, model_validator


class BucketsObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["buckets"] = "buckets"
    buckets: int

    @model_validator(mode='after')
    def check_top(self):
        if self.buckets < 2:
            raise ValueError('Number of buckets must be greater than or equal to 2')
        return self
