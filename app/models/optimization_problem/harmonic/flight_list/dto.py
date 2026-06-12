from typing import List

from app.models.fitness.dto import FitnessDTO
from app.models.optimization_problem.harmonic.target_time_assignment.dto import TargetTimeAssignmentDTO
from .base import FlightListBase


class FlightListInputDTO(FlightListBase):
    target_time_assignments: List[TargetTimeAssignmentDTO]


class FlightListOutputDTO(FlightListInputDTO):
    fitness_list: List[FitnessDTO]
