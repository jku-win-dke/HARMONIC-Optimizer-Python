from typing import List

from app.models.base_mapper import BaseMapper
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from .dto import TargetTimeAssignmentDTO
from .obj import TargetTimeAssignment


class TargetTimeAssignmentMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: TargetTimeAssignment) -> TargetTimeAssignmentDTO:
        return TargetTimeAssignmentDTO(
            target_time_id=obj.target_time.target_time_id,
            flight_id=obj.flight.flight_id
        )

    @staticmethod
    def from_dto(dto: TargetTimeAssignmentDTO, flights: List[Flight], target_times: List[TargetTime]) -> TargetTimeAssignment:
        flight_ref = None
        for flight in flights:
            if flight.flight_id == dto.flight_id:
                flight_ref = flight

        target_time_ref = None
        for target_time in target_times:
            if target_time.target_time_id == dto.target_time_id:
                target_time_ref = target_time

        return TargetTimeAssignment(
            target_time=target_time_ref,
            flight=flight_ref
        )
