from app.models.base_mapper import BaseMapper

from .dto import QuantilesObfuscationDTO
from .obj import QuantilesObfuscation


class QuantilesObfuscationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: QuantilesObfuscation) -> QuantilesObfuscationDTO:
        return QuantilesObfuscationDTO(quantiles=obj.quantiles)

    @staticmethod
    def from_dto(dto: QuantilesObfuscationDTO) -> QuantilesObfuscation:
        return QuantilesObfuscation(quantiles=dto.quantiles)
