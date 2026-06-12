from typing import List

import numpy as np

from app.models.fitness.obj import Fitness
from app.models.solution.obj import Solution
from .base import PopulationBase


class Population(PopulationBase):
    solutions: List[Solution] = []
    filtered: bool = False

    def get_unique_solutions(self) -> List[Solution]:
        solution_groups: dict = {}
        for solution in self.solutions:
            # set all negative placeholder values to None
            modified_encoding = np.where(np.array(solution.encoding) < 0, None, solution.encoding)
            encoding_tuple = tuple(modified_encoding)

            if solution_groups.get(encoding_tuple) is None:
                solution_groups[encoding_tuple] = []

            solution_groups[encoding_tuple].append(solution)

        unique_solutions: List[Solution] = []

        # if there are duplicate solutions, choose the maximum fitness of each objective
        for encoding, solutions in solution_groups.items():
            fitness_dict: dict[str, Fitness] = {}
            for solution in solutions:
                for fitness in solution.fitness_list:
                    if fitness_dict.get(fitness.objective_id) is None:
                        fitness_dict[fitness.objective_id] = Fitness(
                            objective_id=fitness.objective_id,
                            actual_fitness=fitness.actual_fitness,
                            estimated_fitness=fitness.estimated_fitness)
                    else:
                        if (fitness_dict[fitness.objective_id].actual_fitness is None
                                or fitness.actual_fitness > fitness_dict[fitness.objective_id].actual_fitness):
                            fitness_dict[fitness.objective_id].actual_fitness = fitness.actual_fitness

                        if (fitness_dict[fitness.objective_id].estimated_fitness is None
                                or fitness.estimated_fitness > fitness_dict[fitness.objective_id].estimated_fitness):
                            fitness_dict[fitness.objective_id].estimated_fitness = fitness.estimated_fitness

            modified_encoding = np.where(np.array(encoding) == None, -1, encoding).tolist()
            unique_solution = Solution(encoding=modified_encoding, fitness_list=list(fitness_dict.values()))
            unique_solutions.append(unique_solution)

        return unique_solutions

    def get_pareto_optimal_solutions(self) -> List[Solution]:
        pareto_optimal_solutions: List[Solution] = []
        solutions = self.get_unique_solutions()

        for solution in solutions:
            is_pareto_optimal = True

            fitness = np.array(
                [fitness.get_estimated_or_actual_fitness() for fitness in solution.fitness_list])

            for comparison_solution in solutions:
                if solution == comparison_solution:
                    continue

                comparison_fitness = np.array(
                    [fitness.get_estimated_or_actual_fitness() for fitness in comparison_solution.fitness_list])

                # Solution is dominated if for all objectives the fitness values are smaller or equal to
                # the fitness values of the comparison solution
                dominated = np.all(fitness <= comparison_fitness)

                # Solution is strictly dominated if it is dominated and the fitness value for one harmonic_objective
                # is smaller than the fitness value of the comparison solution
                strictly_dominated = dominated and np.any(fitness < comparison_fitness)

                if strictly_dominated:
                    is_pareto_optimal = False
                    break

            if is_pareto_optimal:
                pareto_optimal_solutions.append(solution)

        return pareto_optimal_solutions
