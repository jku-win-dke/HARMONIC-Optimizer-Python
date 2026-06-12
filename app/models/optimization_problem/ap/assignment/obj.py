from typing import List

from app.models.fitness.obj import Fitness
from .base import AssignmentBase


class Assignment(AssignmentBase):
    fitness_list: List[Fitness] = None
