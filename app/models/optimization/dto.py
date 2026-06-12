from typing import Union

from pydantic import Field

from app.models.optimization_framework.pygad.dto import PygadFrameworkDTO
from app.models.optimization_framework.scipy.dto import ScipyFrameworkDTO
from app.models.optimization_problem.ap.dto import AssignmentProblemInputDTO, AssignmentProblemOutputDTO, \
    AssignmentProblemOutputResultDTO
from app.models.optimization_problem.harmonic.dto import HarmonicProblemInputDTO, HarmonicProblemOutputDTO, \
    HarmonicProblemOutputResultDTO
from app.models.optimization_statistics.dto import StatisticsDTO
from .base import OptimizationBase, OptimizationCreatedBase


class OptimizationInputDTO(OptimizationBase):
    problem: Union[
        HarmonicProblemInputDTO,
        AssignmentProblemInputDTO] = Field(
        discriminator='problem_type'
    )
    framework: Union[
        ScipyFrameworkDTO,
        PygadFrameworkDTO,] = Field(
        discriminator='framework_type',
        default=ScipyFrameworkDTO()
    )


class OptimizationOutputDTO(OptimizationCreatedBase):
    problem: Union[HarmonicProblemOutputDTO, AssignmentProblemOutputDTO]
    framework: Union[ScipyFrameworkDTO, PygadFrameworkDTO]
    statistics: StatisticsDTO


class OptimizationOutputBaseDTO(OptimizationCreatedBase):
    pass


class OptimizationOutputStatisticsDTO(OptimizationCreatedBase):
    statistics: StatisticsDTO


class OptimizationOutputResultDTO(OptimizationCreatedBase):
    problem: Union[HarmonicProblemOutputResultDTO, AssignmentProblemOutputResultDTO]
