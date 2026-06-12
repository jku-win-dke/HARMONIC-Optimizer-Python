import random
from typing import Tuple

import numpy as np
import pygad


def partially_matched_crossover(parents: np.ndarray, offspring_size: Tuple, ga_instance: pygad.GA) -> np.ndarray:
    # based on Jenetics 8.1.0-2024
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

        # add 1 to the chromosome_length to include the last element in the range
        chromosome_length = parent_one.shape[0]
        start_idx, end_idx = sorted(random.sample(range(chromosome_length + 1), 2))

        # initialize the offspring with parent one as the base
        offspring = np.full(chromosome_length, np.nan)
        offspring[start_idx:end_idx] = parent_one[start_idx:end_idx]

        # try to insert the genes from parent two that are not in the offspring
        # if the gene is already in the offspring, try to insert the gene from the other parent
        for i in range(len(offspring)):
            if i < start_idx or i >= end_idx:
                gene_to_swap = parent_two[i]

                if gene_to_swap not in offspring:
                    offspring[i] = gene_to_swap
                else:
                    alternative_gene_idx = np.where(offspring == gene_to_swap)[0][0]
                    gene_to_swap = parent_two[alternative_gene_idx]

                    while gene_to_swap in offspring:
                        alternative_gene_idx = np.where(offspring == gene_to_swap)[0][0]
                        gene_to_swap = parent_two[alternative_gene_idx]

                    offspring[i] = gene_to_swap

        offsprings.append(offspring)

    return np.array(offsprings)
