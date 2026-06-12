from typing import List, Optional

import numpy as np

from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.flight_list.obj import FlightList
from app.models.optimization_problem.harmonic.objective.obj import HarmonicObjective
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_assignment.obj import TargetTimeAssignment
from app.models.optimization_problem.obj import OptimizationProblem
from app.models.solution.obj import Solution
from .base import HarmonicProblemBase


class HarmonicProblem(HarmonicProblemBase, OptimizationProblem):
    flights: List[Flight]
    target_times: List[TargetTime]
    objectives: List[HarmonicObjective]
    initial_flight_list: Optional[FlightList]
    result_flight_lists: List[FlightList] = []

    def __init__(self, /, **data):
        super().__init__(**data)

        self.flights = sorted(self.flights, key=lambda flight: flight.flight_id)
        self.target_times = sorted(self.target_times, key=lambda target_time: target_time.target_time_id)

        for objective in self.objectives:
            objective.init_evaluation_setup(self.flights, self.target_times)

        # Compute fitness of initial flight list
        if self.initial_flight_list:
            encoding = self.get_initial_solution()
            self.initial_flight_list.fitness_list = []
            for objective in self.objectives:
                if not objective.privacy_engine:
                    self.initial_flight_list.fitness_list.append(objective.get_fitness(encoding=encoding))

    def get_initial_solution(self) -> List[int] | None:
        if self.initial_flight_list:
            initial_solution = np.full(self.get_problem_size(), -1).tolist()
            for target_time_assignment in self.initial_flight_list.target_time_assignments:
                if len(self.flights) >= len(self.target_times):
                    initial_solution[self.flights.index(target_time_assignment.flight)] = (
                        self.target_times.index(target_time_assignment.target_time))
                else:
                    initial_solution[self.target_times.index(target_time_assignment.target_time)] = (
                        self.flights.index(target_time_assignment.flight))
            return initial_solution
        return None

    def get_problem_size(self) -> int:
        if len(self.flights) >= len(self.target_times):
            return len(self.flights)
        else:
            return len(self.target_times)

    def get_gene_space(self) -> List[int]:
        gene_space = list(range(min(len(self.flights), len(self.target_times))))

        diff = abs(len(self.flights) - len(self.target_times))
        if diff > 0:
            for i in range(diff):
                gene_space.append(-1 - i)

        return gene_space

    def allow_duplicate_genes(self) -> bool:
        return False

    def update_result(self, solutions: List[Solution]) -> None:
        temp_result_flight_lists = []

        for solution in solutions:
            target_time_assignments: List[TargetTimeAssignment] = []

            for flight_idx, tta_idx in enumerate(solution.encoding):
                # If there are more target times than flights, the indices need to be swapped to get the correct assignment
                # This is due to situational representation of the objective
                if len(self.target_times) > len(self.flights):
                    flight_idx, tta_idx = tta_idx, flight_idx

                # check for a valid assignment
                if flight_idx > -1 and tta_idx > -1:
                    target_time_assignments.append(
                        TargetTimeAssignment(target_time=self.target_times[tta_idx],
                                             flight=self.flights[flight_idx])
                    )

            target_time_assignments = sorted(target_time_assignments, key=lambda x: x.target_time.target_time_id)
            flight_list = FlightList(target_time_assignments=target_time_assignments,
                                     fitness_list=solution.fitness_list)
            temp_result_flight_lists.append(flight_list)

        self.result_flight_lists = temp_result_flight_lists
