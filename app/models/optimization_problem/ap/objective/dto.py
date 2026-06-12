from typing import List

from app.models.optimization_objective.dto import OptimizationObjectiveDTO
from .base import AssignmentObjectiveBase


class AssignmentObjectiveDTO(AssignmentObjectiveBase, OptimizationObjectiveDTO):
    weights: List[List[int]]
