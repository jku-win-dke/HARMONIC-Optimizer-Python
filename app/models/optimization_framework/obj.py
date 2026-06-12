import multiprocessing
from abc import abstractmethod
from typing import List

from app.models.optimization_problem.obj import OptimizationProblem
from .base import OptimizationFrameworkBase


class OptimizationFramework(OptimizationFrameworkBase):
    @abstractmethod
    def execute(self, problem: OptimizationProblem, populations: List, queue: multiprocessing.Queue) -> None:
        pass
