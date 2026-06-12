from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import AboveObfuscationBase


class AboveObfuscation(AboveObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeClassification/{self.threshold}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        minimum_fitness = min(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        indices_sorted_individuals = sorted(
            range(len(fitness_values)), # Create a list of indices
            key=lambda i: (fitness_values[i], i), # sort by fitness value and then by index
            reverse=True # sort in descending order
        )

        fitness_threshold = minimum_fitness + ((maximum_fitness - minimum_fitness) * (self.threshold / 100))
        individuals_above_threshold = [i for i in indices_sorted_individuals if fitness_values[i] >= fitness_threshold]

        # For very small problems, less than 3 solutions may be available
        if len(fitness_list) > 3:
            # At least 3 individuals must satisfy the threshold. If not, the next n solutions are added
            # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10253978
            if len(individuals_above_threshold) < 3:
                for i in range(len(individuals_above_threshold), 3):
                    individuals_above_threshold.append(indices_sorted_individuals[i])
        for i, fitness in enumerate(fitness_list):
            fitness.estimated_fitness = maximum_fitness if i in individuals_above_threshold else estimated_min_fitness

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        indices_above_threshold = response['indices']
        maximum_fitness = response['highest']

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        for i in range(len(population.solutions)):
            estimated_fitness = maximum_fitness if i in indices_above_threshold else estimated_min_fitness
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
