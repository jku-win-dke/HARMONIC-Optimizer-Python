import multiprocessing
import random
from datetime import datetime
from typing import List, Callable

import numpy as np
from pygad import pygad

from app.models.optimization_framework.obj import OptimizationFramework
from app.models.optimization_framework.pygad.base import PygadFrameworkBase
from app.models.optimization_problem.obj import OptimizationProblem
from app.models.population.obj import Population
from app.models.solution.obj import Solution


class PygadFramework(PygadFrameworkBase, OptimizationFramework):

    @staticmethod
    def _batch_fitness_function_factory(problem: OptimizationProblem, populations: List[Population]) -> Callable:
        """
        Factory method for creating the fitness function for the genetic algorithm.
        :param problem: OptimizationProblem object
        :return: Fitness function for the genetic algorithm
        """

        def _fitness_function(ga_instance: pygad.GA, solutions: List, solution_indices: List) -> np.ndarray:
            """
            Fitness function for the genetic algorithm.
            :param ga_instance: PyGAD instance
            :param solutions: Solutions to evaluate
            :param solution_indices: Indices of the solutions
            :return: Fitness of the solutions
            """
            # get the current population
            population = populations[-1]

            # add unique solutions to the population
            unique_solutions_dict = {}
            for i, solution in enumerate(solutions):
                # create modified encoding by setting -1 as the gene value for any minus value
                modified_encoding = np.where(np.array(solution) < 0, -1, solution)
                modified_encoding_tuple = tuple(modified_encoding)

                if unique_solutions_dict.get(modified_encoding_tuple) is None:
                    unique_solutions_dict[modified_encoding_tuple] = []
                    population.solutions.append(Solution(encoding=modified_encoding.tolist()))

                unique_solutions_dict[modified_encoding_tuple].append(i)

            # evaluate the population
            population = problem.evaluate_population(population)

            # store the evaluated population
            populations[-1] = population

            # retrieve estimated or actual fitness values from population for single-objective
            if len(problem.objectives) == 1:
                fitness_array = np.zeros(len(solutions))
                for solution in population.solutions:
                    encoding_tuple = tuple(solution.encoding)
                    fitness_array[unique_solutions_dict[encoding_tuple]] = solution.fitness_list[0].get_estimated_or_actual_fitness()
            # retrieve estimated or actual fitness values from population for multi-objective
            else:
                fitness_array = np.zeros((len(solutions), len(problem.objectives)))
                for solution in population.solutions:
                    encoding_tuple = tuple(solution.encoding)
                    for i, fitness in enumerate(solution.fitness_list):
                        fitness_array[unique_solutions_dict[encoding_tuple], i] = fitness.get_estimated_or_actual_fitness()

            return fitness_array

        return _fitness_function

    @staticmethod
    def _on_start_factory(populations: List[Population]) -> Callable:
        def _on_start(ga_instance: pygad.GA) -> None:
            population: Population = Population(population_id=0)
            population.start_time = datetime.now()
            populations.append(population)

        return _on_start

    @staticmethod
    def _on_stop_factory(populations: List[Population], queue: multiprocessing.Queue) -> Callable:
        def _on_stop(ga_instance: pygad.GA, last_population_fitness) -> None:
            previous_population = populations[-1]
            previous_population.end_time = datetime.now()
            populations[-1] = previous_population

            # put the last population id into the queue for further processing
            queue.put(previous_population.population_id)

        return _on_stop

    @staticmethod
    def _on_fitness_factory(populations: List[Population], queue: multiprocessing.Queue) -> Callable:
        def _on_fitness(ga_instance: pygad.GA, population_fitness: List) -> None:
            current_time = datetime.now()

            previous_population = populations[-1]
            previous_population.end_time = current_time
            populations[-1] = previous_population

            # put the previous population id into the queue for further processing
            queue.put(previous_population.population_id)

            population: Population = Population(population_id=ga_instance.generations_completed + 1)
            population.start_time = current_time
            populations.append(population)

        return _on_fitness

    def execute(self, problem: OptimizationProblem, populations: List[Population], queue: multiprocessing.Queue) -> None:
        gene_space = problem.get_gene_space()
        problem_size = problem.get_problem_size()

        # generate initial population
        initial_population = []
        initial_solution = problem.get_initial_solution()
        if initial_solution:
            initial_population.append(initial_solution)

        if self.random_seed is not None:
            random.seed(self.random_seed)

        for _ in range(self.sol_per_pop - len(initial_population)):
            permutation = random.sample(gene_space, problem_size)
            initial_population.append(permutation)

        ga_instance = pygad.GA(
            num_generations=self.num_generations,
            num_parents_mating=self.num_parents_mating,
            fitness_func=self._batch_fitness_function_factory(problem=problem, populations=populations),
            fitness_batch_size=self.sol_per_pop,
            initial_population=initial_population,
            sol_per_pop=self.sol_per_pop,
            num_genes=problem_size,
            gene_type=int,
            init_range_low=self.init_range_low,
            init_range_high=self.init_range_high,
            parent_selection_type=self.parent_selection_mapping,
            keep_parents=self.keep_parents,
            keep_elitism=self.keep_elitism,
            K_tournament=self.K_tournament,
            crossover_type=self.crossover_type_mapping,
            crossover_probability=self.crossover_probability,
            mutation_type=self.mutation_type_mapping,
            mutation_probability=self.mutation_probability,
            mutation_by_replacement=self.mutation_by_replacement,
            mutation_percent_genes=self.mutation_percent_genes,
            mutation_num_genes=self.mutation_num_genes,
            random_mutation_min_val=self.random_mutation_min_val,
            random_mutation_max_val=self.random_mutation_max_val,
            gene_space=gene_space,
            on_start=self._on_start_factory(populations=populations),
            on_stop=self._on_stop_factory(populations=populations, queue=queue),
            on_fitness=self._on_fitness_factory(populations=populations, queue=queue),
            save_best_solutions=self.save_best_solutions,
            save_solutions=self.save_solutions,
            suppress_warnings=False,
            allow_duplicate_genes=problem.allow_duplicate_genes(),
            stop_criteria=self.stop_criteria,
            parallel_processing=self.parallel_processing,
            random_seed=self.random_seed,
            logger=None
        )

        ga_instance.run()

        # stop the filtering process
        queue.put(-1)
