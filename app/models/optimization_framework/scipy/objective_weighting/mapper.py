from app.models.base_mapper import BaseMapper
from app.models.optimization_framework.scipy.objective_weight.mapper import ObjectiveWeightMapper
from app.models.optimization_framework.scipy.objective_weighting.dto import ObjectiveWeightingDTO
from app.models.optimization_framework.scipy.objective_weighting.obj import ObjectiveWeighting


class ObjectiveWeightingMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: ObjectiveWeighting) -> ObjectiveWeightingDTO:
        objective_weights = [ObjectiveWeightMapper.to_dto(weight) for weight in obj.objective_weights]

        return ObjectiveWeightingDTO(
            objective_weights=objective_weights,
        )

    @staticmethod
    def from_dto(dto: ObjectiveWeightingDTO) -> ObjectiveWeighting:
        objective_weights = [ObjectiveWeightMapper.from_dto(weight) for weight in dto.objective_weights]

        return ObjectiveWeighting(
            objective_weights=objective_weights,
        )
