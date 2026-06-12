from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import BucketsObfuscationBase


class BucketsObfuscation(BucketsObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeBuckets/{self.buckets}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        minimum_fitness = min(fitness_values)
        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.buckets - 1))
        span = (maximum_fitness - minimum_fitness) + 1

        for fitness in fitness_list:
            bucket = ((fitness.actual_fitness - minimum_fitness) * self.buckets) // span
            fitness.estimated_fitness = round(estimated_min_fitness + (bucket * distance))

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        maximum_fitness = response['maximum']
        obfuscated_fitness = response['mapping']

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.buckets - 1))

        for i in range(len(population.solutions)):
            estimated_fitness = round(estimated_min_fitness + (distance * obfuscated_fitness[i]))
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
