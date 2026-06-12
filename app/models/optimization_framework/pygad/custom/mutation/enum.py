import enum

from app.models.optimization_framework.pygad.custom.mutation.shift1 import shift_mutation_1
from app.models.optimization_framework.pygad.custom.mutation.shift2 import shift_mutation_2


class CustomMutationOperators(enum.Enum):
    SHIFT_1 = ('shift1', shift_mutation_1)
    SHIFT_2 = ('shift2', shift_mutation_2)
