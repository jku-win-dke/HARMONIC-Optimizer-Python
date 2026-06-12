import pytest

from app.models.fitness.obj import Fitness
from app.models.obfuscation.above.obj import AboveObfuscation
from app.models.obfuscation.buckets.obj import BucketsObfuscation
from app.models.obfuscation.order.obj import OrderObfuscation
from app.models.obfuscation.quantiles.obj import QuantilesObfuscation
from app.models.obfuscation.top.obj import TopObfuscation


@pytest.fixture
def fitness_list():
    return [
        Fitness(objective_id='1', actual_fitness=10),
        Fitness(objective_id='1', actual_fitness=20),
        Fitness(objective_id='1', actual_fitness=30),
        Fitness(objective_id='1', actual_fitness=40),
        Fitness(objective_id='1', actual_fitness=50),
        Fitness(objective_id='1', actual_fitness=60),
        Fitness(objective_id='1', actual_fitness=60),
        Fitness(objective_id='1', actual_fitness=80),
        Fitness(objective_id='1', actual_fitness=90),
        Fitness(objective_id='1', actual_fitness=100),
    ]


def test_above_threshold_obfuscation(fitness_list):
    obfuscation = AboveObfuscation(threshold=80)

    obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

    assert fitness_list[0].estimated_fitness == -100
    assert fitness_list[1].estimated_fitness == -100
    assert fitness_list[2].estimated_fitness == -100
    assert fitness_list[3].estimated_fitness == -100
    assert fitness_list[4].estimated_fitness == -100
    assert fitness_list[5].estimated_fitness == -100
    assert fitness_list[6].estimated_fitness == -100
    assert fitness_list[7].estimated_fitness == 100
    assert fitness_list[8].estimated_fitness == 100
    assert fitness_list[9].estimated_fitness == 100


def test_order_obfuscation(fitness_list):
    obfuscation = OrderObfuscation()

    obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

    assert fitness_list[0].estimated_fitness == -100
    assert fitness_list[1].estimated_fitness == -78
    assert fitness_list[2].estimated_fitness == -56
    assert fitness_list[3].estimated_fitness == -33
    assert fitness_list[4].estimated_fitness == -11
    assert fitness_list[5].estimated_fitness == 11
    assert fitness_list[6].estimated_fitness == 33
    assert fitness_list[7].estimated_fitness == 56
    assert fitness_list[8].estimated_fitness == 78
    assert fitness_list[9].estimated_fitness == 100


def test_top_solutions_obfuscation(fitness_list):
    obfuscation = TopObfuscation(top=4)

    obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

    assert fitness_list[0].estimated_fitness == -100
    assert fitness_list[1].estimated_fitness == -100
    assert fitness_list[2].estimated_fitness == -100
    assert fitness_list[3].estimated_fitness == -100
    assert fitness_list[4].estimated_fitness == -100
    assert fitness_list[5].estimated_fitness == -100
    assert fitness_list[6].estimated_fitness == 100
    assert fitness_list[7].estimated_fitness == 100
    assert fitness_list[8].estimated_fitness == 100
    assert fitness_list[9].estimated_fitness == 100


def test_order_quantiles_obfuscation(fitness_list):
    obfuscation = QuantilesObfuscation(quantiles=5)

    obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

    assert fitness_list[0].estimated_fitness == -100
    assert fitness_list[1].estimated_fitness == -100
    assert fitness_list[2].estimated_fitness == -50
    assert fitness_list[3].estimated_fitness == -50
    assert fitness_list[4].estimated_fitness == 0
    assert fitness_list[5].estimated_fitness == 0
    assert fitness_list[6].estimated_fitness == 50
    assert fitness_list[7].estimated_fitness == 50
    assert fitness_list[8].estimated_fitness == 100
    assert fitness_list[9].estimated_fitness == 100


def test_fitness_range_obfuscation(fitness_list):
    obfuscation = BucketsObfuscation(buckets=5)

    obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

    assert fitness_list[0].estimated_fitness == -100
    assert fitness_list[1].estimated_fitness == -100
    assert fitness_list[2].estimated_fitness == -50
    assert fitness_list[3].estimated_fitness == -50
    assert fitness_list[4].estimated_fitness == 0
    assert fitness_list[5].estimated_fitness == 0
    assert fitness_list[6].estimated_fitness == 0
    assert fitness_list[7].estimated_fitness == 50
    assert fitness_list[8].estimated_fitness == 100
    assert fitness_list[9].estimated_fitness == 100
