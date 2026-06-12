from app.models.base_mapper import BaseMapper

from .dto import TopObfuscationDTO
from .obj import TopObfuscation


class TopObfuscationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: TopObfuscation) -> TopObfuscationDTO:
        return TopObfuscationDTO(top=obj.top)

    @staticmethod
    def from_dto(dto: TopObfuscationDTO) -> TopObfuscation:
        return TopObfuscation(top=dto.top)
