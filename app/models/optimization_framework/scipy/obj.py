import concurrent.futures
import multiprocessing
from datetime import datetime
from typing import List, Optional, Dict, Union

import numpy as np
from scipy.optimize import linear_sum_assignment

from app.models.optimization_framework.obj import OptimizationFramework
from app.models.optimization_problem.harmonic.obj import HarmonicProblem
from app.models.population.obj import Population
from app.models.solution.obj import Solution
from app.models.optimization_problem.ap.obj import AssignmentProblem
from .base import ScipyFrameworkBase
from .objective_weight.obj import ObjectiveWeight
from .objective_weighting.obj import ObjectiveWeighting


class ScipyFramework(ScipyFrameworkBase, OptimizationFramework):
    objective_weightings: Optional[List[ObjectiveWeighting]] = None

    @staticmethod
    def _execute(objective_weighting: ObjectiveWeighting, normalized_matrices: Dict, problem: HarmonicProblem, maximize: bool) -> Solution:
        # combine objective_weight matrix for given weights
        combined_weight_matrix = np.zeros_like(normalized_matrices.get(list(normalized_matrices.keys())[0]))

        for objective_weight in objective_weighting.objective_weights:
            combined_weight_matrix += objective_weight.weight * normalized_matrices[objective_weight.objective_id]

        # compute an optimal solution
        row_ind, col_ind = linear_sum_assignment(cost_matrix=combined_weight_matrix, maximize=maximize)

        # not every flight may have a tta assigned and vice versa
        encoding: np.ndarray = np.full(problem.get_problem_size(), -1, dtype=int)
        for i in range(len(row_ind)):
            encoding[row_ind[i]] = col_ind[i]

        # evaluate and return solution
        return problem.evaluate_solution(Solution(encoding=encoding.tolist()))

    def execute(self, problem: Union[HarmonicProblem, AssignmentProblem], populations: List[Population], queue: multiprocessing.Queue) -> None:
        for objective in problem.objectives:
            if objective.privacy_engine or objective.obfuscation:
                raise RuntimeError("ScipyFramework does not support privacy engine or obfuscation")

        # normalize matrices of objectives (if available) based on true min and max values
        normalized_matrices: dict = {}
        for objective in problem.objectives:
            min_value = np.min(objective.matrix)
            max_value = np.max(objective.matrix)

            if max_value != min_value:
                # normalize matrix based on true min and max values
                normalized_matrices[objective.objective_id] = (objective.matrix - min_value) / (
                        max_value - min_value)
            else:
                # if all values are equal, set them to 1
                normalized_matrices[objective.objective_id] = np.ones_like(objective.matrix)

        # if no weightings are provided, use the same weight for each objective
        objective_weightings = self.objective_weightings
        if objective_weightings is None or len(objective_weightings) == 0:
            objective_weighting = ObjectiveWeighting(objective_weights=[])
            weight = 1.0 / len(problem.objectives)
            for objective in problem.objectives:
                objective_weighting.objective_weights.append(
                    ObjectiveWeight(objective_id=objective.objective_id, weight=weight))
            objective_weightings = [objective_weighting]

        # only 1 population object with scipy
        population = Population(population_id=0, start_time=datetime.now())

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(ScipyFramework._execute, objective_weighting, normalized_matrices, problem, self.maximize):
                           objective_weighting for objective_weighting in objective_weightings}

            for future in concurrent.futures.as_completed(futures):
                population.solutions.append(future.result())

        population.end_time = datetime.now()

        populations.append(population)

        queue.put(population.population_id)

        # stop the filtering process
        queue.put(-1)
