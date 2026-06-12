from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import QuantilesObfuscationBase


class QuantilesObfuscation(QuantilesObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeQuantiles/{self.quantiles}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.quantiles - 1))

        indices_sorted_individuals = sorted(
            range(len(fitness_values)), # Create a list of indices
            key=lambda i: (fitness_values[i], i), # sort by fitness value and then by index
            reverse=False # sort in ascending order
        )

        obfuscated_fitness = [(idx, (i * self.quantiles) // len(fitness_values)) for i, idx in enumerate(indices_sorted_individuals)]
        obfuscated_fitness.sort(key=(lambda x: x[0]))
        obfuscated_fitness = [x[1] for x in obfuscated_fitness] # Extract the quantile_assignment

        for i, fitness in enumerate(fitness_list):
            fitness.estimated_fitness = round(estimated_min_fitness + (distance * obfuscated_fitness[i]))

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        maximum_fitness = response['maximum']
        obfuscated_fitness = response['mapping']

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.quantiles - 1))

        for i in range(len(population.solutions)):
            estimated_fitness = round(estimated_min_fitness + (distance * obfuscated_fitness[i]))
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
