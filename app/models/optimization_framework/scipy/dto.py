from typing import List, Optional

from app.models.optimization_framework.dto import OptimizationFrameworkDTO
from .base import ScipyFrameworkBase
from .objective_weighting.dto import ObjectiveWeightingDTO


class ScipyFrameworkDTO(ScipyFrameworkBase, OptimizationFrameworkDTO):
    objective_weightings: Optional[List[ObjectiveWeightingDTO]] = None
