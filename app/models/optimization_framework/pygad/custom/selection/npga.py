import random
import pygad
import numpy as np

from typing import Tuple
from app.models.optimization_framework.pygad.custom.selection.utils import strictly_dominates


def npga_selection(fitness: np.ndarray, num_parents: int, ga_instance: pygad.GA, comparison_sample_size: int, niche_radius: float) -> Tuple[np.ndarray, np.ndarray]:
    # based on Horn et al. (1997)
    # https://ieeexplore.ieee.org/abstract/document/350037
    # see Horn & Nafpliotis (1993) for pseudo code and recommendations of the comparison sample size
    # https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=785fef2ed791b6aed643299500f2c3dba43beede

    # normalize fitness for niche counting
    # limitation: fitness is normalized based on the current population
    normalized_fitness = np.zeros_like(fitness, dtype=float)
    for i in range(fitness.shape[1]):
        objective_values = fitness[:, i]
        min_value = objective_values.min()
        max_value = objective_values.max()
        normalized_fitness[:, i] = (objective_values - min_value) / (max_value - min_value)

    parent_indices = []

    for parent_num in range(num_parents):
        rand_indices = random.sample(range(len(fitness)), 2 + comparison_sample_size)

        candidate_1 = rand_indices[0]
        candidate_2 = rand_indices[1]
        comparison_set = rand_indices[2:]

        candidate_1_dominated = False
        candidate_2_dominated = False
        for i in range(len(comparison_set)):
            comparison_individual = comparison_set[i]

            if strictly_dominates(fitness[comparison_individual], fitness[candidate_1]):
                candidate_1_dominated = True

            if strictly_dominates(fitness[comparison_individual], fitness[candidate_2]):
                candidate_2_dominated = True

            if candidate_1_dominated and candidate_2_dominated:
                break

        if not candidate_1_dominated and candidate_2_dominated:
            parent_indices.append(candidate_1)

        elif candidate_1_dominated and not candidate_2_dominated:
            parent_indices.append(candidate_2)

        else:
            candidate_1_niche_count = 0
            candidate_2_niche_count = 0

            for i in range(len(comparison_set)):
                comparison_individual = comparison_set[i]

                if np.linalg.norm(
                        normalized_fitness[candidate_1] - normalized_fitness[comparison_individual]) <= niche_radius:
                    candidate_1_niche_count += 1

                if np.linalg.norm(
                        normalized_fitness[candidate_2] - normalized_fitness[comparison_individual]) <= niche_radius:
                    candidate_2_niche_count += 1

            if candidate_1_niche_count < candidate_2_niche_count:
                parent_indices.append(candidate_1)

            else:
                parent_indices.append(candidate_2)

    parents = np.array(ga_instance.population[parent_indices])

    return parents, np.array(parent_indices)
