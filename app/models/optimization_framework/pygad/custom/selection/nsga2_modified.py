from typing import Tuple, Generator, Iterator

import numpy as np
import pygad


def non_dominated_sorting_modified(fitness: np.ndarray, ga_instance: pygad.GA):
    # verify the multi-objectiveness of the problem
    if type(fitness[0]) not in [list, tuple, np.ndarray]:
        raise TypeError('no multi-objective optimization problem')

    remaining_set = fitness.copy()
    # zipping the solution indices with their corresponding fitness values
    remaining_set = list(zip(range(0, fitness.shape[0]), remaining_set))

    front_index = -1
    while len(remaining_set) > 0:
        front_index += 1

        # get the current non-dominated set of solutions
        pareto_front, remaining_set = ga_instance.get_non_dominated_set(curr_solutions=remaining_set)
        pareto_front = np.array(pareto_front, dtype=object)

        yield pareto_front


def nsga2_selection_modified(fitness: np.ndarray, num_parents: int, ga_instance: pygad.GA) -> Tuple[np.ndarray, np.ndarray]:
    """
    copied and adapted from pygad to only compute the required number of pareto-optimal fronts
    """
    # verify the multi-objectiveness of the problem
    if type(fitness[0]) not in [list, tuple, np.ndarray]:
        raise TypeError('no multi-objective optimization problem')

    # retrieves only the next pareto front
    generator_non_dominated_sorting = non_dominated_sorting_modified(fitness, ga_instance)

    selected_parents = []

    # collect the pareto fronts until the desired number of parents is reached
    while len(selected_parents) < num_parents:
        current_front = next(generator_non_dominated_sorting)

        if len(selected_parents) + len(current_front) <= num_parents:
            selected_parents.extend(current_front)

        else:
            # calculate the crowding distance of the current front
            (obj_crowding_distance_list,
             crowding_distance_sum,
             crowding_dist_front_sorted_indices,
             crowding_dist_pop_sorted_indices
             ) = ga_instance.crowding_distance(pareto_front=current_front.copy(), fitness=fitness)

            # select the best solutions based on the crowding distance
            num_parents_missing = num_parents - len(selected_parents)
            selected_indices = crowding_dist_pop_sorted_indices[:num_parents_missing]

            front_indices = [f[0] for f in current_front]
            for i in selected_indices:
                if i in front_indices:
                    index = front_indices.index(i)
                    selected_parents.append(current_front[index])

    ga_instance.pareto_fronts = selected_parents.copy()

    parents_indices = [parent[0] for parent in selected_parents]
    parents = ga_instance.population[parents_indices]

    return parents, np.array(parents_indices)
