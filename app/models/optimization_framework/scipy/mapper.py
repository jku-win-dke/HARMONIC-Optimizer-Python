from app.models.base_mapper import BaseMapper

from .dto import ScipyFrameworkDTO
from .obj import ScipyFramework
from .objective_weighting.mapper import ObjectiveWeightingMapper


class ScipyFrameworkMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: ScipyFramework) -> ScipyFrameworkDTO:
        weightings = None
        if obj.objective_weightings:
            weightings = [ObjectiveWeightingMapper.to_dto(weighting) for weighting in obj.objective_weightings]

        return ScipyFrameworkDTO(
            objective_weightings=weightings,
            maximize=obj.maximize,
        )

    @staticmethod
    def from_dto(dto: ScipyFrameworkDTO) -> ScipyFramework:
        weightings = None
        if dto.objective_weightings:
            weightings = [ObjectiveWeightingMapper.from_dto(weighting) for weighting in dto.objective_weightings]

        return ScipyFramework(
            objective_weightings=weightings,
            maximize=dto.maximize,
        )
