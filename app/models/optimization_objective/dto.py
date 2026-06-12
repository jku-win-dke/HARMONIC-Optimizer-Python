from abc import ABC
from typing import Optional, Union

from pydantic import Field

from app.models.obfuscation.above.dto import AboveObfuscationDTO
from app.models.obfuscation.buckets.dto import BucketsObfuscationDTO
from app.models.obfuscation.order.dto import OrderObfuscationDTO
from app.models.obfuscation.quantiles.dto import QuantilesObfuscationDTO
from app.models.obfuscation.top.dto import TopObfuscationDTO
from app.models.optimization_objective.base import OptimizationObjectiveBase


class OptimizationObjectiveDTO(OptimizationObjectiveBase, ABC):
    obfuscation: Optional[
        Union[
            OrderObfuscationDTO,
            TopObfuscationDTO,
            AboveObfuscationDTO,
            QuantilesObfuscationDTO,
            BucketsObfuscationDTO,]
    ] = Field(
        discriminator='obfuscation_type',
        default=None)
