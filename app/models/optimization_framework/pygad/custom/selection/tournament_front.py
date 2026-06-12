import random
from typing import Tuple

import numpy as np
import pygad

from app.models.optimization_framework.pygad.custom.selection.utils import strictly_dominates


def tournament_front_selection(fitness: np.ndarray, num_parents: int, ga_instance: pygad.GA) -> Tuple[np.ndarray, np.ndarray]:
    parent_indices = []

    for parent_num in range(num_parents):
        # select random indices of individuals to compete in the tournament
        participant_indices = random.sample(range(len(fitness)), ga_instance.K_tournament)

        # calculate the pareto optimal participant indices
        pareto_optimal_participant_indices = []
        for i in range(len(participant_indices)):
            current_participant_idx = participant_indices[i]
            is_strictly_dominated = False

            for j in range(len(participant_indices)):
                if i == j:
                    continue

                comparison_participant_idx = participant_indices[j]

                if strictly_dominates(fitness[comparison_participant_idx], fitness[current_participant_idx]):
                    is_strictly_dominated = True
                    break

            if not is_strictly_dominated:
                pareto_optimal_participant_indices.append(current_participant_idx)

        # select a random solution from the pareto optimal participants
        winner_participant_idx = random.choice(pareto_optimal_participant_indices)
        parent_indices.append(winner_participant_idx)

    parents = np.array(ga_instance.population[parent_indices])

    return parents, np.array(parent_indices)
