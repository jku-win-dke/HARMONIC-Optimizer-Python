from typing import List

from app.models.fitness.obj import Fitness
from app.models.optimization_problem.harmonic.target_time_assignment.obj import TargetTimeAssignment
from .base import FlightListBase


class FlightList(FlightListBase):
    target_time_assignments: List[TargetTimeAssignment]
    fitness_list: List[Fitness] = None
