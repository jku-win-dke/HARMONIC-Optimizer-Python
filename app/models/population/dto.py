from typing import List

from app.models.solution.dto import SolutionDTO
from .base import PopulationBase


class PopulationDTO(PopulationBase):
    solutions: List[SolutionDTO] = []
