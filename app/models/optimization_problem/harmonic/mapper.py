from app.models.optimization_problem.harmonic.flight.mapper import FlightMapper
from app.models.optimization_problem.harmonic.flight_list.mapper import FlightListMapper
from app.models.optimization_problem.harmonic.objective.mapper import HarmonicObjectiveMapper
from app.models.optimization_problem.harmonic.target_time.mapper import TargetTimeMapper
from app.models.optimization_problem.problem_mapper import OptimizationProblemMapper

from .dto import HarmonicProblemInputDTO, HarmonicProblemOutputDTO, HarmonicProblemOutputResultDTO
from .obj import HarmonicProblem


class HarmonicProblemMapper(OptimizationProblemMapper):
    @staticmethod
    def to_dto(obj: HarmonicProblem) -> HarmonicProblemOutputDTO:
        flights = [FlightMapper.to_dto(flight) for flight in obj.flights]
        target_times = [TargetTimeMapper.to_dto(target_time) for target_time in obj.target_times]

        objectives = [HarmonicObjectiveMapper.to_dto(objective) for objective in obj.objectives]

        initial_flight_list = None
        if obj.initial_flight_list:
            initial_flight_list = FlightListMapper.to_dto(obj.initial_flight_list)

        result_flight_lists = [FlightListMapper.to_dto(flight_list) for flight_list in obj.result_flight_lists]

        return HarmonicProblemOutputDTO(
            flights=flights,
            target_times=target_times,
            objectives=objectives,
            initial_flight_list=initial_flight_list,
            result_flight_lists=result_flight_lists,
        )

    @staticmethod
    def to_result_dto(obj: HarmonicProblem) -> HarmonicProblemOutputResultDTO:
        flights = [FlightMapper.to_dto(flight) for flight in obj.flights]
        target_times = [TargetTimeMapper.to_dto(target_time) for target_time in obj.target_times]

        result_flight_lists = [FlightListMapper.to_dto(flight_list) for flight_list in obj.result_flight_lists]

        return HarmonicProblemOutputResultDTO(
            flights=flights,
            target_times=target_times,
            result_flight_lists=result_flight_lists,
        )

    @staticmethod
    def from_dto(dto: HarmonicProblemInputDTO) -> HarmonicProblem:
        flights = [FlightMapper.from_dto(flight) for flight in dto.flights]
        target_times = [TargetTimeMapper.from_dto(target_time) for target_time in dto.target_times]

        objectives = [
            HarmonicObjectiveMapper.from_dto(objective, flights, target_times)
            for objective in dto.objectives
        ]

        initial_flight_list = None
        if dto.initial_flight_list:
            initial_flight_list = FlightListMapper.from_dto(dto.initial_flight_list, flights, target_times)

        return HarmonicProblem(
            flights=flights,
            target_times=target_times,
            objectives=objectives,
            initial_flight_list=initial_flight_list,
        )
