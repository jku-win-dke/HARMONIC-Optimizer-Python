from app.models.base_mapper import BaseMapper
from app.models.optimization_framework.scipy.objective_weight.dto import ObjectiveWeightDTO
from app.models.optimization_framework.scipy.objective_weight.obj import ObjectiveWeight


class ObjectiveWeightMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: ObjectiveWeight) -> ObjectiveWeightDTO:
        return ObjectiveWeightDTO(
            objective_id=obj.objective_id,
            weight=obj.weight,
        )

    @staticmethod
    def from_dto(dto: ObjectiveWeightDTO) -> ObjectiveWeight:
        return ObjectiveWeight(
            objective_id=dto.objective_id,
            weight=dto.weight,
        )
