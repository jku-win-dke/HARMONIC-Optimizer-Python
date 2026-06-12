from app.models.base_mapper import BaseMapper

from .dto import TargetTimeDTO
from .obj import TargetTime


class TargetTimeMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: TargetTime) -> TargetTimeDTO:
        return TargetTimeDTO(
            target_time_id=obj.target_time_id,
            time=obj.time
        )

    @staticmethod
    def from_dto(dto: TargetTimeDTO) -> TargetTime:
        return TargetTime(
            target_time_id=dto.target_time_id,
            time=dto.time
        )
