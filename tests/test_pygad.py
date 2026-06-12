import numpy as np
import pytest
from pygad import pygad

from app.models.optimization_framework.pygad.custom.crossover.pmx import partially_matched_crossover
from app.models.optimization_framework.pygad.custom.crossover.uox import uniform_order_based_crossover
from app.models.optimization_framework.pygad.custom.mutation.shift1 import shift_mutation_1
from app.models.optimization_framework.pygad.custom.mutation.shift2 import shift_mutation_2
from app.models.optimization_framework.pygad.custom.selection.npga import npga_selection
from app.models.optimization_framework.pygad.custom.selection.nsga2_modified import nsga2_selection_modified
from app.models.optimization_framework.pygad.custom.selection.spea2 import spea2_selection
from app.models.optimization_framework.pygad.custom.selection.tournament_ko import tournament_ko_selection
from app.models.optimization_framework.pygad.custom.selection.tournament_front import \
    tournament_front_selection


@pytest.fixture
def data():
    return np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]])


@pytest.fixture
def data_tournament():
    data = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
    fitness = np.array([[100, 0], [100, 10], [90, 20], [30, 30], [50, 50], [45, 45], [30, 30], [20, 90], [10, 100], [0, 100]])

    return data, fitness


@pytest.fixture
def ga_instance():
    def dummy_fitness_func(ga_instance, solutions, solution_indices):
        return 0

    # Create a dummy GA instance
    ga_instance = pygad.GA(crossover_probability=None, num_generations=1, num_parents_mating=1,
                           sol_per_pop=1, num_genes=10, fitness_func=dummy_fitness_func, K_tournament=4,
                           mutation_num_genes=3, random_seed=42)

    return ga_instance


def test_partially_matched_crossover(data, ga_instance):
    data_copy = data.copy()
    offspring = partially_matched_crossover(parents=data_copy, offspring_size=data.shape, ga_instance=ga_instance)

    assert offspring.shape == data.shape
    assert np.array_equal(offspring[0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert np.array_equal(offspring[1], [10, 9, 8, 7, 5, 6, 4, 3, 2, 1])
    assert len(set(offspring[0])) == len(data[0])
    assert len(set(offspring[1])) == len(data[1])


def test_uniform_order_based_crossover(data, ga_instance):
    data_copy = data.copy()
    offspring = uniform_order_based_crossover(parents=data_copy, offspring_size=data.shape, ga_instance=ga_instance, keep_genes_probability=0.5)

    assert offspring.shape == data.shape
    assert np.array_equal(offspring[0], [1, 8, 3, 4, 5, 6, 7, 2, 9, 10])
    assert np.array_equal(offspring[1], [2, 9, 8, 7, 6, 3, 4, 5, 10, 1])
    assert len(set(offspring[0])) == len(data[0])
    assert len(set(offspring[1])) == len(data[1])


def test_shift_mutation1(data, ga_instance):
    data_copy = data.copy()
    offspring = shift_mutation_1(offspring=data_copy, ga_instance=ga_instance)

    assert offspring.shape == data.shape
    assert np.array_equal(offspring[0], [2, 3, 4, 1, 5, 6, 7, 8, 9, 10])
    assert np.array_equal(offspring[1], [10, 9, 8, 6, 5, 4, 7, 3, 2, 1])
    assert len(set(offspring[0])) == len(data[0])
    assert len(set(offspring[1])) == len(data[1])


def test_shift_mutation2(data, ga_instance):
    data_copy = data.copy()
    offspring = shift_mutation_2(offspring=data_copy, ga_instance=ga_instance)

    assert offspring.shape == data.shape
    assert np.array_equal(offspring[0], [1, 3, 4, 2, 5, 6, 7, 8, 9, 10])
    assert np.array_equal(offspring[1], [10, 9, 8, 7, 5, 4, 6, 3, 2, 1])
    assert len(set(offspring[0])) == len(data[0])
    assert len(set(offspring[1])) == len(data[1])


def test_binary_pareto_tournament(data_tournament, ga_instance):
    data, fitness = data_tournament
    ga_instance.population = data

    parents, parents_indices = tournament_ko_selection(fitness=fitness, num_parents=ga_instance.num_parents_mating, ga_instance=ga_instance)

    expected_parent = np.array([2])
    expected_index = 1

    assert np.array_equal(parents[0], expected_parent)
    assert parents_indices == expected_index


def test_pareto_optimal_tournament(data_tournament, ga_instance):
    data, fitness = data_tournament
    ga_instance.population = data

    parents, parents_indices = tournament_front_selection(fitness=fitness, num_parents=ga_instance.num_parents_mating, ga_instance=ga_instance)

    expected_parent = np.array([2])
    expected_index = 1

    assert np.array_equal(parents[0], expected_parent)
    assert parents_indices == expected_index


def test_nsga2_modified(data_tournament, ga_instance):
    data, fitness = data_tournament
    ga_instance.population = data

    parents, parents_indices = nsga2_selection_modified(fitness=fitness, num_parents=ga_instance.num_parents_mating, ga_instance=ga_instance)

    expected_parent = np.array([2])
    expected_index = 1

    assert np.array_equal(parents[0], expected_parent)
    assert parents_indices == expected_index

    # Test with 5 parents
    parents, parents_indices = nsga2_selection_modified(fitness=fitness, num_parents=5, ga_instance=ga_instance)

    expected_parents = np.array([[2], [3], [5], [8], [9]])
    expected_indices = [1, 2, 4, 7, 8]

    assert np.array_equal(parents, expected_parents)
    assert np.array_equal(parents_indices, expected_indices)


def test_npga_selection(data_tournament, ga_instance):
    data, fitness = data_tournament
    ga_instance.population = data

    parents, parents_indices = npga_selection(fitness=fitness, num_parents=ga_instance.num_parents_mating, ga_instance=ga_instance, comparison_sample_size=2, niche_radius=1)

    expected_parent = np.array([1])
    expected_index = 0

    assert np.array_equal(parents[0], expected_parent)
    assert parents_indices == expected_index

    # Test with 3 parents
    parents, parents_indices = npga_selection(fitness=fitness, num_parents=3, ga_instance=ga_instance, comparison_sample_size=2, niche_radius=1)

    expected_parents = np.array([[3], [9], [2]])
    expected_indices = [2, 8, 1]

    assert np.array_equal(parents, expected_parents)
    assert np.array_equal(parents_indices, expected_indices)


def test_spea2_selection(data_tournament, ga_instance):
    data, fitness = data_tournament
    archive = []
    ga_instance.population = data

    parents, parents_indices = spea2_selection(fitness=fitness, num_parents=ga_instance.num_parents_mating, ga_instance=ga_instance, archive=archive, archive_size=2)

    expected_parent = np.array([2])
    expected_index = 1

    assert np.array_equal(archive[0][0], np.array([2]))
    assert np.array_equal(archive[0][1], np.array([100, 10]))
    assert np.array_equal(archive[1][0], np.array([9]))
    assert np.array_equal(archive[1][1], np.array([10, 100]))
    assert np.array_equal(parents[0], expected_parent)
    assert parents_indices == expected_index
