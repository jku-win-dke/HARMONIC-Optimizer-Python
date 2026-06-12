from typing import List

from app.models.optimization_framework.scipy.objective_weight.obj import ObjectiveWeight
from app.models.optimization_framework.scipy.objective_weighting.base import ObjectiveWeightingBase


class ObjectiveWeighting(ObjectiveWeightingBase):
    objective_weights: List[ObjectiveWeight]
