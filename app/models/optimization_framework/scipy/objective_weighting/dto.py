from typing import List

from app.models.optimization_framework.scipy.objective_weight.dto import ObjectiveWeightDTO
from app.models.optimization_framework.scipy.objective_weighting.base import ObjectiveWeightingBase


class ObjectiveWeightingDTO(ObjectiveWeightingBase):
    objective_weights: List[ObjectiveWeightDTO]
