from typing import List

from app.models.base_mapper import BaseMapper
from app.models.fitness.mapper import FitnessMapper
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_assignment.mapper import TargetTimeAssignmentMapper
from .dto import FlightListOutputDTO, FlightListInputDTO
from .obj import FlightList

class FlightListMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: FlightList) -> FlightListOutputDTO:
        target_time_assignments = [TargetTimeAssignmentMapper.to_dto(target_time_assignment)
                                   for target_time_assignment in obj.target_time_assignments]

        fitness_list = [FitnessMapper.to_dto(fitness)
                        for fitness in obj.fitness_list]

        return FlightListOutputDTO(
            target_time_assignments=target_time_assignments,
            fitness_list=fitness_list,
        )

    @staticmethod
    def from_dto(dto: FlightListInputDTO, flights: List[Flight], target_times: List[TargetTime]) -> FlightList:
        target_time_assignments = [TargetTimeAssignmentMapper.from_dto(target_time_assignment, flights, target_times)
                                   for target_time_assignment in dto.target_time_assignments]

        return FlightList(
            target_time_assignments=target_time_assignments,
        )
