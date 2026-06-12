from abc import ABC
from typing import Optional

from pydantic import BaseModel, AnyUrl, model_validator


class OptimizationObjectiveBase(ABC, BaseModel):
    objective_id: str
    privacy_engine: Optional[AnyUrl] = None
    encoding_url: Optional[AnyUrl] = None

    @model_validator(mode='after')
    def check_privacy_engine_and_encoding_url(self):
        if self.privacy_engine and not self.encoding_url:
            raise ValueError('encoding_url must be set when privacy_engine is set')
        if self.encoding_url and not self.privacy_engine:
            raise ValueError('privacy_engine must be set when encoding_url is set')
        return self
