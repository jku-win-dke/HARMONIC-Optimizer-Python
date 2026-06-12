from app.models.base_mapper import BaseMapper

from .dto import OrderObfuscationDTO
from .obj import OrderObfuscation


class OrderObfuscationMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: OrderObfuscation) -> OrderObfuscationDTO:
        return OrderObfuscationDTO()

    @staticmethod
    def from_dto(dto: OrderObfuscationDTO) -> OrderObfuscation:
        return OrderObfuscation()
