from typing import List

from app.models.fitness.obj import Fitness
from .base import SolutionBase


class Solution(SolutionBase):
    encoding: List[int]
    fitness_list: List[Fitness] = []
