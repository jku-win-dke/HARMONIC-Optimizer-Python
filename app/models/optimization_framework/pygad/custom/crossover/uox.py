import random
from collections import deque
from typing import Tuple

import numpy as np
import pygad


def uniform_order_based_crossover(parents: np.ndarray, offspring_size: Tuple, ga_instance: pygad.GA, keep_genes_probability: float) -> np.ndarray:
    offsprings = []

    for k in range(offspring_size[0]):
        if ga_instance.crossover_probability is not None:
            probs = np.random.random(size=parents.shape[0])
            indices = list(set(np.where(probs <= ga_instance.crossover_probability)[0]))

            # if no parent satisfied the probability, no crossover is applied and a parent is selected
            if len(indices) == 0:
                offsprings.append(parents[k % parents.shape[0], :].copy())
                continue
            elif len(indices) == 1:
                parent1_idx = indices[0]
                parent2_idx = indices[0]
            else:
                indices = random.sample(indices, 2)
                parent1_idx = indices[0]
                parent2_idx = indices[1]
        else:
            # index of the first parent to mate
            parent1_idx = k % parents.shape[0]
            # index of the second parent to mate
            parent2_idx = (k + 1) % parents.shape[0]

        parent_one = parents[parent1_idx, :].copy()
        parent_two = parents[parent2_idx, :].copy()

        # create a random mask based on the keep_genes_probability to determine which genes are being kept
        mask = np.random.rand(parents.shape[1]) <= keep_genes_probability

        # initialize the offspring with the kept genes from parent one as base
        offspring = np.full(parents.shape[1], np.nan)
        used_gene_values = set()
        for i in range(parents.shape[1]):
            if mask[i]:
                gene_value = parent_one[i]
                offspring[i] = gene_value
                used_gene_values.add(gene_value)

        # fill the remaining gene values in the order of the second parent
        remaining_gene_values = deque([gene_value for gene_value in parent_two if gene_value not in used_gene_values])
        for i in range(parents.shape[1]):
            if not mask[i]:
                offspring[i] = remaining_gene_values.popleft()

        offsprings.append(offspring)

    return np.array(offsprings)
