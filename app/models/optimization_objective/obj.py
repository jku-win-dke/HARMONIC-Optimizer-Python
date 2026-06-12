from abc import ABC, abstractmethod
from typing import Optional, List

import numpy as np
import requests
from requests.exceptions import ConnectionError

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.optimization_objective.base import OptimizationObjectiveBase
from app.models.population.obj import Population


class OptimizationObjective(OptimizationObjectiveBase, ABC):
    obfuscation: Optional[Obfuscation] = None

    @abstractmethod
    def _get_fitness(self, encoding: List[int]) -> Fitness:
        pass

    def get_fitness(self, encoding: List[int]) -> Fitness:
        if self.privacy_engine is None:
            return self._get_fitness(encoding)

        return Fitness(objective_id=self.objective_id, actual_fitness=None)

    def get_evaluation_result(self, population: Population) -> List[Fitness]:
        fitness_list = []

        if self.privacy_engine is None:

            for solution in population.solutions:
                fitness_list.append(self._get_fitness(encoding=solution.encoding))

            if self.obfuscation:
                fitness_list = self.obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

        else:
            try:
                response = requests.get(f'{self.privacy_engine}/status')
                if response.status_code == 200:

                    # if it is an imbalanced problem, modify solution encodings for the privacy engine
                    solution_encodings = [solution.encoding for solution in population.solutions]
                    if min(solution_encodings[0]) < 0:
                        dummy_value = max(solution_encodings[0]) + 1
                        solution_encodings = np.where(np.array(solution_encodings) < 0, dummy_value,
                                                      solution_encodings).tolist()

                    if self.obfuscation is None:
                        request = requests.put(f'{self.privacy_engine}/computeFitnessClear', json=solution_encodings)

                        if request.status_code == 200:
                            response = request.json()
                            for i in range(len(population.solutions)):
                                fitness_list.append(
                                    Fitness(objective_id=self.objective_id, actual_fitness=response[i]))
                        else:
                            raise RuntimeError(
                                f'No valid response from privacy engine. Status code: {request.status_code}')

                    else:
                        request = requests.put(f'{self.privacy_engine}/{self.obfuscation.endpoint_privacy_engine}',
                                               json=solution_encodings)

                        if request.status_code == 200:
                            response = request.json()
                            fitness_list = self.obfuscation.estimate_based_on_privacy_engine(response=response,
                                                                                             population=population,
                                                                                             objective_id=self.objective_id)
                            for i, solution in enumerate(population.solutions):
                                fitness_list[i].actual_fitness = self._get_fitness(
                                    encoding=solution.encoding).actual_fitness
                        else:
                            raise RuntimeError(
                                f'No valid response from privacy engine. Status code: {request.status_code}')
                else:
                    raise RuntimeError(
                        f'Privacy Engine for objective {self.objective_id} is available but not reachable')
            except ConnectionError as e:
                raise RuntimeError(f'Privacy Engine for objective {self.objective_id} is not available')

        return fitness_list
