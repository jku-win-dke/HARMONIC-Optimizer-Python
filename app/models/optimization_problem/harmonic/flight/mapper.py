from app.models.base_mapper import BaseMapper

from .dto import FlightDTO
from .obj import Flight


class FlightMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Flight) -> FlightDTO:
        return FlightDTO(
            flight_id=obj.flight_id,
            scheduled_time=obj.scheduled_time
        )

    @staticmethod
    def from_dto(dto: FlightDTO) -> Flight:
        return Flight(
            flight_id=dto.flight_id,
            scheduled_time=dto.scheduled_time
        )
