import numpy as np


def strictly_dominates(fitness_list_1: np.ndarray, fitness_list_2: np.ndarray) -> bool:
    # A solution dominates another one if it is no worse in all objectives and strictly better in at least one objective
    no_worse_in_all = all(f1 >= f2 for f1, f2 in zip(fitness_list_1, fitness_list_2))
    strictly_better_in_one = any(f1 > f2 for f1, f2 in zip(fitness_list_1, fitness_list_2))
    return no_worse_in_all and strictly_better_in_one
