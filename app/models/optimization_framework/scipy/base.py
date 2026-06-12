from abc import ABC
from typing import Literal

from pydantic import BaseModel


class ScipyFrameworkBase(ABC, BaseModel):
    framework_type: Literal["scipy"] = "scipy"
    maximize: bool = True
