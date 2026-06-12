import random
from typing import Tuple

import numpy as np
import pygad

from app.models.optimization_framework.pygad.custom.selection.utils import strictly_dominates


def tournament_ko_selection(fitness: np.ndarray, num_parents: int, ga_instance: pygad.GA) -> Tuple[np.ndarray, np.ndarray]:
    parent_indices = []

    for parent_num in range(num_parents):
        # select random indices of individuals to compete in the tournament
        nominated_participant_indices = random.sample(range(len(fitness)), ga_instance.K_tournament)

        # two solutions compete against each other until only one remains
        while len(nominated_participant_indices) > 1:
            winner_participant_indices = []

            # if the number of participants is odd, the last individual receives a free pass for the next round
            if len(nominated_participant_indices) % 2 == 1:
                # shuffle to reduce bias
                random.shuffle(nominated_participant_indices)
                winner_participant_indices.append(nominated_participant_indices[-1])
                nominated_participant_indices = nominated_participant_indices[:-1]

            for i in range(0, len(nominated_participant_indices), 2):
                individual_1_idx = nominated_participant_indices[i]
                individual_2_idx = nominated_participant_indices[i + 1]

                # determine the winner of a pair
                if strictly_dominates(fitness[individual_1_idx], fitness[individual_2_idx]):
                    winner_participant_indices.append(individual_1_idx)
                elif strictly_dominates(fitness[individual_2_idx], fitness[individual_1_idx]):
                    winner_participant_indices.append(individual_2_idx)
                else:
                    winner_participant_indices.append(random.choice([individual_1_idx, individual_2_idx]))

            # the winners compete in the next round
            nominated_participant_indices = winner_participant_indices

        parent_indices.append(nominated_participant_indices[0])

    parents = np.array(ga_instance.population[parent_indices])

    return parents, np.array(parent_indices)
