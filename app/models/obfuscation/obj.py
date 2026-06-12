from abc import abstractmethod, ABC
from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.population.obj import Population
from .base import ObfuscationBase


class Obfuscation(ObfuscationBase, ABC):

    @abstractmethod
    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        pass

    @abstractmethod
    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        pass
