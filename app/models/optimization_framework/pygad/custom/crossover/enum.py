import enum

from app.models.optimization_framework.pygad.custom.crossover.pmx import partially_matched_crossover
from app.models.optimization_framework.pygad.custom.crossover.uox import uniform_order_based_crossover


class CustomCrossoverOperators(enum.Enum):
    PMX = ('pmx', partially_matched_crossover)
    UOX = ('uox', uniform_order_based_crossover)
