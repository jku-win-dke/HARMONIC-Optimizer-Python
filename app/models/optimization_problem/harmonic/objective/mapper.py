from typing import List

from app.models.base_mapper import BaseMapper
from app.models.obfuscation.registry import ObfuscationMapperRegistry
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.flight_preferences.mapper import FlightPreferencesMapper
from app.models.optimization_problem.harmonic.objective.dto import HarmonicObjectiveDTO
from app.models.optimization_problem.harmonic.objective.obj import HarmonicObjective
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime


class HarmonicObjectiveMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: HarmonicObjective) -> HarmonicObjectiveDTO:
        flight_preferences = [FlightPreferencesMapper.to_dto(preference) for preference in obj.flight_preferences]

        obfuscation = None
        if obj.obfuscation:
            obfuscation = (ObfuscationMapperRegistry.get_mapper(obj.obfuscation.obfuscation_type)
                           .to_dto(obj=obj.obfuscation))

        return HarmonicObjectiveDTO(
            objective_id=obj.objective_id,
            privacy_engine=obj.privacy_engine,
            flight_preferences=flight_preferences,
            obfuscation=obfuscation,
            encoding_url=obj.encoding_url
        )

    @staticmethod
    def from_dto(dto: HarmonicObjectiveDTO, flights: List[Flight], target_times: List[TargetTime]) -> HarmonicObjective:
        flight_preferences = [FlightPreferencesMapper.from_dto(preference, flights, target_times)
                              for preference in dto.flight_preferences]

        obfuscation = None
        if dto.obfuscation:
            obfuscation = (ObfuscationMapperRegistry.get_mapper(dto.obfuscation.obfuscation_type)
                           .from_dto(dto=dto.obfuscation))

        return HarmonicObjective(
            objective_id=dto.objective_id,
            privacy_engine=dto.privacy_engine,
            flight_preferences=flight_preferences,
            obfuscation=obfuscation,
            encoding_url=dto.encoding_url
        )
