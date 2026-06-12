import random
import pygad
import numpy as np

from typing import Tuple
from app.models.optimization_framework.pygad.custom.selection.utils import strictly_dominates


def spea2_selection(fitness: np.ndarray, num_parents: int, ga_instance: pygad.GA, archive: list, archive_size: int) -> Tuple[np.ndarray, np.ndarray]:
    # based on Zitzler et al. (2001)
    # https://sop.tik.ee.ethz.ch/publicationListFiles/zlt2001a.pdf

    # Combine the encodings and fitness of the archived solutions and the population
    if archive:
        combined_population = np.vstack([archived_solution[0] for archived_solution in archive])
        combined_population = np.vstack((combined_population, ga_instance.population))

        combined_fitness = np.vstack([archived_solution[1] for archived_solution in archive])
        combined_fitness = np.vstack((combined_fitness, fitness))

    else:
        combined_population = ga_instance.population.copy()
        combined_fitness = fitness.copy()

    # Only consider unique encodings
    unique_encodings = []
    duplicate_solutions_indices = []

    for i, solution in enumerate(combined_population):
        modified_encoding = tuple(np.where(np.array(solution) < 0, -1, solution))
        if modified_encoding in unique_encodings:
            duplicate_solutions_indices.append(i)
        else:
            unique_encodings.append(modified_encoding)

    combined_population = np.delete(combined_population, duplicate_solutions_indices, axis=0)
    combined_fitness = np.delete(combined_fitness, duplicate_solutions_indices, axis=0)

    population_size = len(combined_population)

    # Compute the strength values
    strength = np.zeros(population_size)
    for i in range(population_size):
        for j in range(population_size):
            if i != j and strictly_dominates(combined_fitness[i], combined_fitness[j]):
                strength[i] += 1

    # Compute the raw fitness based on strength values
    raw_fitness = np.zeros(population_size)
    for i in range(population_size):
        for j in range(population_size):
            if i != j and strictly_dominates(combined_fitness[j], combined_fitness[i]):
                raw_fitness[i] += strength[j]

    # Compute the matrix of Euclidean distances
    distances = np.zeros((population_size, population_size))
    for i in range(population_size):
        for j in range(population_size):
            if i != j:
                distances[i, j] = np.linalg.norm(combined_fitness[i] - combined_fitness[j])

    # Compute the densities based on k-nearest neighbors
    densities = np.zeros(population_size)
    k = int(np.sqrt(population_size))
    for i in range(population_size):
        sorted_distances = np.sort(distances[i])
        densities[i] = 1 / (sorted_distances[k] + 2)

    # Compute the fitness values
    fitness_values = raw_fitness + densities

    # Select unique indices of solutions with fitness < 1
    temp_indices = []
    for i in range(population_size):
        if fitness_values[i] < 1:
            temp_indices.append(i)

    # Fill archive with the best solutions having fitness >= 1
    if len(temp_indices) < archive_size:
        indices_fitness_values_sorted = np.argsort(fitness_values)
        for i in range(len(temp_indices), archive_size if archive_size < population_size else population_size):
            temp_indices.append(indices_fitness_values_sorted[i])

    # Remove solutions from the archive based on the specified truncation operation
    elif len(temp_indices) > archive_size:
        while len(temp_indices) > archive_size:
            selected_distances = distances[:, temp_indices]
            min_distance_index = temp_indices[0]
            sorted_min_distances = sorted(selected_distances[min_distance_index])

            for i in range(1, len(temp_indices)):
                comparison_index = temp_indices[i]
                sorted_distances = sorted(selected_distances[comparison_index])
                for a, b in zip(sorted_min_distances, sorted_distances):
                    if a < b:
                        break
                    elif a > b:
                        min_distance_index = comparison_index
                        sorted_min_distances = sorted_distances
                        break

            # Remove the solution with the minimum distance
            temp_indices.remove(min_distance_index)

    # Update the archive
    temp_archive = []
    for i in range(len(temp_indices)):
        temp_archive.append((combined_population[temp_indices[i]], combined_fitness[temp_indices[i]]))
    archive[:] = temp_archive

    # Perform binary tournament selection to select the parents
    parents_indices = []
    for parent_num in range(num_parents):
        # Generate random indices for the candidate solutions to compete from the archive
        rand_indices = random.sample(range(len(archive)), 2)

        # Select the fitness values of the candidate solutions
        fitness_candidate_1 = fitness_values[temp_indices[rand_indices[0]]]
        fitness_candidate_2 = fitness_values[temp_indices[rand_indices[1]]]

        if fitness_candidate_1 < fitness_candidate_2:
            parents_indices.append(temp_indices[rand_indices[0]])
        elif fitness_candidate_2 < fitness_candidate_1:
            parents_indices.append(temp_indices[rand_indices[1]])
        else:
            if np.random.random() < 0.5:
                parents_indices.append(temp_indices[rand_indices[0]])
            else:
                parents_indices.append(temp_indices[rand_indices[1]])

    selected_parents = np.array(combined_population[parents_indices])

    new_population = selected_parents
    new_fitness = combined_fitness[parents_indices]

    # Modify the population and fitness to contain the selected parents
    # If the number of selected parents is smaller than the solutions per population, placeholder solutions are added to the population
    if len(new_population) < ga_instance.sol_per_pop:
        num_additional_solutions = ga_instance.sol_per_pop - len(new_population)

        placeholder_solutions = np.full((num_additional_solutions, ga_instance.num_genes), -1)
        placeholder_fitness = np.full((num_additional_solutions, len(new_fitness[0])), -1)

        new_population = np.vstack((new_population, placeholder_solutions))
        new_fitness = np.vstack((new_fitness, placeholder_fitness))

    ga_instance.population = new_population
    fitness[:] = new_fitness

    return selected_parents, np.array(parents_indices)
