from typing import List

from app.models.base_mapper import BaseMapper
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_preference.mapper import TargetTimePreferenceMapper
from .dto import FlightPreferencesDTO
from .obj import FlightPreferences


class FlightPreferencesMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: FlightPreferences) -> FlightPreferencesDTO:
        target_time_preferences = [TargetTimePreferenceMapper.to_dto(preference)
                                   for preference in obj.target_time_preferences]

        return FlightPreferencesDTO(
            flight_id=obj.flight.flight_id,
            target_time_preferences=target_time_preferences,
        )

    @staticmethod
    def from_dto(dto: FlightPreferencesDTO, flights: List[Flight], target_times: List[TargetTime]) -> FlightPreferences:
        target_time_preferences = [TargetTimePreferenceMapper.from_dto(preference, target_times)
                                   for preference in dto.target_time_preferences]

        flight_ref = None
        for flight in flights:
            if flight.flight_id == dto.flight_id:
                flight_ref = flight

        return FlightPreferences(
            flight=flight_ref,
            target_time_preferences=target_time_preferences,
        )
