from typing import List

from app.models.fitness.dto import FitnessDTO
from .base import AssignmentBase


class AssignmentDTO(AssignmentBase):
    fitness_list: List[FitnessDTO]
