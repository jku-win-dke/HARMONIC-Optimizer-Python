import pytest

from app.models.fitness.obj import Fitness
from app.models.population.obj import Population
from app.models.solution.obj import Solution


@pytest.fixture
def population():
    return Population(
        population_id=1,
        solutions=[
            Solution(encoding=[1, 2], fitness_list=[
                Fitness(objective_id='1', actual_fitness=100),
                Fitness(objective_id='2', actual_fitness=0)]),
            Solution(encoding=[1, 2], fitness_list=[
                Fitness(objective_id='1', actual_fitness=100),
                Fitness(objective_id='2', actual_fitness=10)]),
            Solution(encoding=[3, 4], fitness_list=[
                Fitness(objective_id='1', actual_fitness=90),
                Fitness(objective_id='2', actual_fitness=20)]),
            Solution(encoding=[5, 6], fitness_list=[
                Fitness(objective_id='1', actual_fitness=50),
                Fitness(objective_id='2', actual_fitness=50)]),
            Solution(encoding=[7, 8], fitness_list=[
                Fitness(objective_id='1', actual_fitness=20),
                Fitness(objective_id='2', actual_fitness=90)]),
            Solution(encoding=[9, 10, -1, -2], fitness_list=[
                Fitness(objective_id='1', actual_fitness=10),
                Fitness(objective_id='2', actual_fitness=100)]),
            Solution(encoding=[9, 10, -2, -1], fitness_list=[
                Fitness(objective_id='1', actual_fitness=20),
                Fitness(objective_id='2', actual_fitness=100)])
        ]
    )

def test_unique_solutions(population):
    unique_solutions = population.get_unique_solutions()

    assert len(unique_solutions) == 5
    assert population.solutions[1] in unique_solutions
    assert population.solutions[2] in unique_solutions
    assert population.solutions[3] in unique_solutions
    assert population.solutions[4] in unique_solutions

    assert unique_solutions[-1].encoding == [9, 10, -1, -1]
    assert unique_solutions[-1].fitness_list[0].actual_fitness == 20
    assert unique_solutions[-1].fitness_list[1].actual_fitness == 100


def test_pareto_optimality(population):
    pareto_optimal_solutions = population.get_pareto_optimal_solutions()

    assert len(pareto_optimal_solutions) == 4
    assert population.solutions[1] in pareto_optimal_solutions
    assert population.solutions[2] in pareto_optimal_solutions
    assert population.solutions[3] in pareto_optimal_solutions

    assert pareto_optimal_solutions[-1].encoding == [9, 10, -1, -1]
    assert pareto_optimal_solutions[-1].fitness_list[0].actual_fitness == 20
    assert pareto_optimal_solutions[-1].fitness_list[1].actual_fitness == 100
