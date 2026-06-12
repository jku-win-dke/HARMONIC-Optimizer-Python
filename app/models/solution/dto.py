from typing import List

from app.models.fitness.dto import FitnessDTO
from .base import SolutionBase


class SolutionDTO(SolutionBase):
    encoding: str
    fitness_list: List[FitnessDTO] = []
