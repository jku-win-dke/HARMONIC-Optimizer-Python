import multiprocessing
from datetime import datetime

import numpy as np
import pytest
from pygad import pygad

from app.models.fitness.obj import Fitness
from app.models.optimization.obj import Optimization
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.flight_preferences.obj import FlightPreferences
from app.models.optimization_problem.harmonic.obj import HarmonicProblem
from app.models.optimization_problem.harmonic.objective.obj import HarmonicObjective
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_preference.obj import TargetTimePreference
from app.models.population.obj import Population
from app.models.solution.obj import Solution


@pytest.fixture
def population():
    return Population(
        population_id=1,
        solutions=[
            Solution(encoding=[1, 2], fitness_list=[
                Fitness(objective_id='1', actual_fitness=100),
                Fitness(objective_id='2', actual_fitness=10)]),
            Solution(encoding=[3, 4], fitness_list=[
                Fitness(objective_id='1', actual_fitness=60),
                Fitness(objective_id='2', actual_fitness=40)]),
            Solution(encoding=[5, 6], fitness_list=[
                Fitness(objective_id='1', actual_fitness=50),
                Fitness(objective_id='2', actual_fitness=50)]),
            Solution(encoding=[7, 8], fitness_list=[
                Fitness(objective_id='1', actual_fitness=40),
                Fitness(objective_id='2', actual_fitness=90)]),
            Solution(encoding=[9, 10], fitness_list=[
                Fitness(objective_id='1', actual_fitness=10),
                Fitness(objective_id='2', actual_fitness=100)]),
            Solution(encoding=[11, 12], fitness_list=[
                Fitness(objective_id='1', actual_fitness=-10),
                Fitness(objective_id='2', actual_fitness=110)]),
            Solution(encoding=[13, 14], fitness_list=[
                Fitness(objective_id='1', actual_fitness=110),
                Fitness(objective_id='2', actual_fitness=-10)]),
        ]
    )

@pytest.fixture
def problem():
    flight_preferences = FlightPreferences(
        flight=Flight(
            flight_id='flight_id',
            scheduled_time=datetime.now()
        ),
        target_time_preferences=[TargetTimePreference(
            target_time=TargetTime(
                target_time_id='target_time_id',
                time=datetime.now()
            ),
            weight=['weight']
        )])


    return HarmonicProblem(
        flights=[],
        target_times=[],
        objectives=[HarmonicObjective(
            objective_id='1',
            flight_preferences=[flight_preferences],
        ),
        HarmonicObjective(
            objective_id='2',
            flight_preferences=[flight_preferences],
        )],
        result_flight_lists=[],
        initial_flight_list=None
    )

@pytest.fixture
def ga_instance():
    def dummy_fitness_func(ga_instance, solutions, solution_indices):
        return 0

    # Create a dummy GA instance
    ga_instance = pygad.GA(crossover_probability=None, num_generations=1, num_parents_mating=1,
                           sol_per_pop=1, num_genes=10, fitness_func=dummy_fitness_func, K_tournament=4,
                           mutation_num_genes=3, random_seed=42)

    return ga_instance


def test_result_filter_no_negatives(population, problem, ga_instance):
    dummy_queue = multiprocessing.Queue()
    dummy_queue.put(0)
    dummy_queue.put(-1)

    population.solutions = population.solutions[:-2]

    results = []
    Optimization.result_filter_process_method(result_queue=dummy_queue,
                                              populations=[population],
                                              time_optimization_stopped=multiprocessing.Value('d', 0.0),
                                              results=results,
                                              result_size=4,
                                              problem=problem)

    fitness = np.array([
        np.array([solution.fitness_list[0].actual_fitness, solution.fitness_list[1].actual_fitness])
        for solution in population.solutions
    ])
    indices_results_pygad = ga_instance.sort_solutions_nsga2(fitness=fitness)
    results_pygad = [population.solutions[i] for i in indices_results_pygad]

    assert len(results) == 4

    assert population.solutions[0] == results[0] == results_pygad[0]
    assert population.solutions[4] == results[1] == results_pygad[1]
    assert population.solutions[1] == results[2]
    assert population.solutions[3] == results[3]

    assert population.solutions[2] not in results
    assert results_pygad[-1] not in results


def test_result_filter_objective_one_negative(population, problem, ga_instance):
    dummy_queue = multiprocessing.Queue()
    dummy_queue.put(0)
    dummy_queue.put(-1)

    population.solutions = population.solutions[:-1] # Remove the solution with negative fitness in objective 2

    results = []
    Optimization.result_filter_process_method(result_queue=dummy_queue,
                                              populations=[population],
                                              time_optimization_stopped=multiprocessing.Value('d', 0.0),
                                              results=results,
                                              result_size=4,
                                              problem=problem)

    fitness = np.array([
        np.array([solution.fitness_list[0].actual_fitness, solution.fitness_list[1].actual_fitness])
        for solution in population.solutions
    ])
    indices_results_pygad = ga_instance.sort_solutions_nsga2(fitness=fitness)
    results_pygad = [population.solutions[i] for i in indices_results_pygad]

    assert len(results) == 4

    assert population.solutions[0] == results[0] == results_pygad[0]
    assert population.solutions[5] == results[1] == results_pygad[1]
    assert population.solutions[3] == results[2]
    assert population.solutions[1] == results[3]

    assert population.solutions[2] not in results
    assert population.solutions[4] not in results
    assert results_pygad[-1] not in results


def test_result_filter_objective_two_negative(population, problem, ga_instance):
    dummy_queue = multiprocessing.Queue()
    dummy_queue.put(0)
    dummy_queue.put(-1)

    del population.solutions[5]  # Remove the solution with negative fitness in objective 1

    results = []
    Optimization.result_filter_process_method(result_queue=dummy_queue,
                                              populations=[population],
                                              time_optimization_stopped=multiprocessing.Value('d', 0.0),
                                              results=results,
                                              result_size=4,
                                              problem=problem)

    fitness = np.array([
        np.array([solution.fitness_list[0].actual_fitness, solution.fitness_list[1].actual_fitness])
        for solution in population.solutions
    ])
    indices_results_pygad = ga_instance.sort_solutions_nsga2(fitness=fitness)
    results_pygad = [population.solutions[i] for i in indices_results_pygad]

    assert len(results) == 4

    assert population.solutions[4] == results[0] == results_pygad[0]
    assert population.solutions[5] == results[1] == results_pygad[1]
    assert population.solutions[0] == results[2]
    assert population.solutions[1] == results[3]

    assert population.solutions[3] not in results
    assert population.solutions[2] not in results
    assert results_pygad[-1] not in results


def test_results_filter_both_objectives_negative(population, problem, ga_instance):
    dummy_queue = multiprocessing.Queue()
    dummy_queue.put(0)
    dummy_queue.put(-1)

    results = []
    Optimization.result_filter_process_method(result_queue=dummy_queue,
                                              populations=[population],
                                              time_optimization_stopped=multiprocessing.Value('d', 0.0),
                                              results=results,
                                              result_size=4,
                                              problem=problem)

    fitness = np.array([
        np.array([solution.fitness_list[0].actual_fitness, solution.fitness_list[1].actual_fitness])
        for solution in population.solutions
    ])
    indices_results_pygad = ga_instance.sort_solutions_nsga2(fitness=fitness)
    results_pygad = [population.solutions[i] for i in indices_results_pygad]

    assert len(results) == 4

    assert population.solutions[5] == results[0] == results_pygad[0]
    assert population.solutions[6] == results[1] == results_pygad[1]
    assert population.solutions[0] == results[2]
    assert population.solutions[1] == results[3]

    assert population.solutions[3] not in results
    assert population.solutions[2] not in results
    assert population.solutions[4] not in results
    assert results_pygad[-1] not in results


def test_results_filter_only_negative_fitness_values(population, problem, ga_instance):
    dummy_queue = multiprocessing.Queue()
    dummy_queue.put(0)
    dummy_queue.put(-1)

    population.solutions = population.solutions[:-2]

    # Change the fitness values to negative
    for solution in population.solutions:
        for fitness in solution.fitness_list:
            fitness.actual_fitness = fitness.actual_fitness * -1

    results = []
    Optimization.result_filter_process_method(result_queue=dummy_queue,
                                              populations=[population],
                                              time_optimization_stopped=multiprocessing.Value('d', 0.0),
                                              results=results,
                                              result_size=4,
                                              problem=problem)

    fitness = np.array([
        np.array([solution.fitness_list[0].actual_fitness, solution.fitness_list[1].actual_fitness])
        for solution in population.solutions
    ])
    indices_results_pygad = ga_instance.sort_solutions_nsga2(fitness=fitness)
    results_pygad = [population.solutions[i] for i in indices_results_pygad]

    assert len(results) == 4

    assert population.solutions[0] == results[0] == results_pygad[0]
    assert population.solutions[4] == results[1] == results_pygad[1]
    assert population.solutions[1] == results[2]
    assert population.solutions[3] == results[3]

    assert population.solutions[2] not in results
    assert results_pygad[-1] not in results
