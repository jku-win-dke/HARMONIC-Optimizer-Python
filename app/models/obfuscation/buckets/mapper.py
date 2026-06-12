from app.models.base_mapper import BaseMapper

from .dto import BucketsObfuscationDTO
from .obj import BucketsObfuscation


class BucketsObfuscationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: BucketsObfuscation) -> BucketsObfuscationDTO:
        return BucketsObfuscationDTO(buckets=obj.buckets)

    @staticmethod
    def from_dto(dto: BucketsObfuscationDTO) -> BucketsObfuscation:
        return BucketsObfuscation(buckets=dto.buckets)
