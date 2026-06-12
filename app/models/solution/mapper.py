from typing import Any

from app.models.base_mapper import BaseMapper
from app.models.fitness.mapper import FitnessMapper
from .dto import SolutionDTO
from .obj import Solution


class SolutionMapper(BaseMapper):

    @staticmethod
    def to_dto(obj: Solution) -> SolutionDTO:
        fitness_list = [FitnessMapper.to_dto(fitness) for fitness in obj.fitness_list]

        return SolutionDTO(
            encoding=str(obj.encoding),
            fitness_list=fitness_list,
        )

    @staticmethod
    def from_dto(**kwargs) -> Any:
        raise Exception("Not implemented")
