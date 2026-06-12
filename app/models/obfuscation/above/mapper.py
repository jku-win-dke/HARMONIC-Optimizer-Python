from app.models.base_mapper import BaseMapper

from .dto import AboveObfuscationDTO
from .obj import AboveObfuscation


class AboveObfuscationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: AboveObfuscation) -> AboveObfuscationDTO:
        return AboveObfuscationDTO(threshold=obj.threshold)

    @staticmethod
    def from_dto(dto: AboveObfuscationDTO) -> AboveObfuscation:
        return AboveObfuscation(threshold=dto.threshold)
