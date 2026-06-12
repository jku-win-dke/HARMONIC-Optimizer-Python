from typing import Any

from app.models.base_mapper import BaseMapper
from app.models.solution.mapper import SolutionMapper
from .dto import PopulationDTO
from .obj import Population


class PopulationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Population) -> PopulationDTO:
        solutions = [SolutionMapper.to_dto(solution) for solution in obj.solutions]

        return PopulationDTO(
            population_id=obj.population_id,
            start_time=obj.start_time,
            end_time=obj.end_time,
            solutions=solutions,
        )

    @staticmethod
    def from_dto(**kwargs) -> Any:
        raise Exception("Not implemented")
