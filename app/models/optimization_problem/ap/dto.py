from typing import List

from app.models.optimization_problem.dto import OptimizationProblemDTO
from .base import AssignmentProblemBase
from .objective.dto import AssignmentObjectiveDTO
from .assignment.dto import AssignmentDTO


class AssignmentProblemInputDTO(AssignmentProblemBase, OptimizationProblemDTO):
    objectives: List[AssignmentObjectiveDTO]


class AssignmentProblemOutputDTO(AssignmentProblemBase, OptimizationProblemDTO):
    objectives: List[AssignmentObjectiveDTO]
    result_assignments: List[AssignmentDTO] = []


class AssignmentProblemOutputResultDTO(AssignmentProblemBase, OptimizationProblemDTO):
    result_assignments: List[AssignmentDTO] = []
