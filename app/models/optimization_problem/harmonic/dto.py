from typing import List, Optional

from pydantic import model_validator

from app.models.optimization_problem.dto import OptimizationProblemDTO
from app.models.optimization_problem.harmonic.flight.dto import FlightDTO
from app.models.optimization_problem.harmonic.flight_list.dto import FlightListInputDTO, FlightListOutputDTO
from app.models.optimization_problem.harmonic.objective.dto import HarmonicObjectiveDTO
from app.models.optimization_problem.harmonic.target_time.dto import TargetTimeDTO
from .base import HarmonicProblemBase


class HarmonicProblemInputDTO(HarmonicProblemBase, OptimizationProblemDTO):
    flights: List[FlightDTO]
    target_times: List[TargetTimeDTO]
    objectives: List[HarmonicObjectiveDTO]
    initial_flight_list: Optional[FlightListInputDTO] = None

    @model_validator(mode='after')
    def check_attributes(self):
        """
        Validates the attributes of the HarmonicProblemDTO.
        - The number of flights and target times must be equal.
        - The target time assignments in the initial flight list must be unique.
        :return: Checked HarmonicProblemDTO
        """

        if self.initial_flight_list is not None:
            used_target_times = set()
            for target_time_assignment in self.initial_flight_list.target_time_assignments:
                if target_time_assignment.target_time_id in used_target_times:
                    raise ValueError('The target time assignments in the initial flight list must be unique.')
                else:
                    used_target_times.add(target_time_assignment.target_time_id)

        return self


class HarmonicProblemOutputDTO(HarmonicProblemBase, OptimizationProblemDTO):
    flights: List[FlightDTO]
    target_times: List[TargetTimeDTO]
    objectives: List[HarmonicObjectiveDTO]
    initial_flight_list: Optional[FlightListOutputDTO] = None
    result_flight_lists: List[FlightListOutputDTO] = []


class HarmonicProblemOutputResultDTO(HarmonicProblemBase, OptimizationProblemDTO):
    flights: List[FlightDTO]
    target_times: List[TargetTimeDTO]
    result_flight_lists: List[FlightListOutputDTO] = []
