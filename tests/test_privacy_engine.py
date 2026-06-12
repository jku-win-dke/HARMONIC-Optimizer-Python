from datetime import datetime

import numpy as np
import pytest

from app.models.fitness.obj import Fitness
from app.models.obfuscation.above.obj import AboveObfuscation
from app.models.obfuscation.buckets.obj import BucketsObfuscation
from app.models.obfuscation.order.obj import OrderObfuscation
from app.models.obfuscation.quantiles.obj import QuantilesObfuscation
from app.models.obfuscation.top.obj import TopObfuscation
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.flight_preferences.obj import FlightPreferences
from app.models.optimization_problem.harmonic.objective.obj import HarmonicObjective
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_preference.obj import TargetTimePreference
from app.models.population.obj import Population
from app.models.solution.obj import Solution


def dummy_flight_preferences():
    return FlightPreferences(
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

def dummy_matrix():
    return np.array([
        [100, 80, 60, 40, 20],
        [90, 70, 50, 30, 10],
        [80, 60, 40, 20, 0],
        [100, 70, 40, 10, -10],
        [50, -1000, -100, 50, 50]
    ])

@pytest.fixture
def harmonic_objective_privacy_engine():
    return HarmonicObjective(
        objective_id='1',
        privacy_engine="http://127.0.0.1:80",
        encoding_url="http://127.0.0.1:88",
        flight_preferences=[dummy_flight_preferences()],
        matrix=dummy_matrix()
    )

@pytest.fixture(autouse=True)
def init_privacy_engine(harmonic_objective_privacy_engine):
    harmonic_objective_privacy_engine.init_evaluation_setup(flights=['flights'], target_times=['target_times'])

@pytest.fixture
def harmonic_objective():
    return HarmonicObjective(
        objective_id='1',
        flight_preferences=[dummy_flight_preferences()],
        matrix=dummy_matrix()
    )

@pytest.fixture
def population():
    return Population(
        population_id=1,
        solutions=[
            Solution(encoding=[0, 1, 2, 3, 4], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[1, 0, 2, 3, 4], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[4, 3, 2, 1, 0], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[1, 0, 2, 4, 3], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[3, 4, 2, 0, 1], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[4, 1, 2, 3, 0], fitness_list=[
                Fitness(objective_id='1')]),
            Solution(encoding=[4, 3, 1, 0, 2], fitness_list=[
                Fitness(objective_id='1')]),
        ])


def test_compute_fitness_clear(harmonic_objective_privacy_engine, harmonic_objective, population):
    fitness_list_fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)

    assert len(fitness_list_fitness_list_privacy_engine) == 7
    assert fitness_list_fitness_list_privacy_engine[0].actual_fitness == fitness_list[0].actual_fitness == 270
    assert fitness_list_fitness_list_privacy_engine[1].actual_fitness == fitness_list[1].actual_fitness == 270
    assert fitness_list_fitness_list_privacy_engine[2].actual_fitness == fitness_list[2].actual_fitness == 210
    assert fitness_list_fitness_list_privacy_engine[3].actual_fitness == fitness_list[3].actual_fitness == 250
    assert fitness_list_fitness_list_privacy_engine[4].actual_fitness == fitness_list[4].actual_fitness == -810
    assert fitness_list_fitness_list_privacy_engine[5].actual_fitness == fitness_list[5].actual_fitness == 190
    assert fitness_list_fitness_list_privacy_engine[6].actual_fitness == fitness_list[6].actual_fitness == 110



def test_order_obfuscation(harmonic_objective_privacy_engine, harmonic_objective, population):
    harmonic_objective_privacy_engine.obfuscation = OrderObfuscation()
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = OrderObfuscation()
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 180
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == 0
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 90
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == -90
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == -180


def test_top_obfuscation(harmonic_objective_privacy_engine, harmonic_objective, population):
    harmonic_objective_privacy_engine.obfuscation = TopObfuscation(top=3)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = TopObfuscation(top=3)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == -270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == -270
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == -270


def test_buckets_obfuscation(harmonic_objective_privacy_engine, harmonic_objective, population):
    harmonic_objective_privacy_engine.obfuscation = BucketsObfuscation(buckets=2)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = BucketsObfuscation(buckets=2)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == 270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == 270
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == 270

    harmonic_objective_privacy_engine.obfuscation = BucketsObfuscation(buckets=15)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = BucketsObfuscation(buckets=15)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == 270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == 231
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == 193


def test_above_obfuscation(harmonic_objective_privacy_engine, harmonic_objective, population):
    # Test that at least 3 individuals satisfy the threshold
    harmonic_objective_privacy_engine.obfuscation = AboveObfuscation(threshold=99)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = AboveObfuscation(threshold=99)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == -270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == -270
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == -270

    harmonic_objective_privacy_engine.obfuscation = AboveObfuscation(threshold=80)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = AboveObfuscation(threshold=80)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == 270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == 270
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == 270


def test_quantiles_obfuscation(harmonic_objective_privacy_engine, harmonic_objective, population):
    harmonic_objective_privacy_engine.obfuscation = QuantilesObfuscation(quantiles=2)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = QuantilesObfuscation(quantiles=2)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 270
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == -270
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 270
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == -270
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == -270

    harmonic_objective_privacy_engine.obfuscation = QuantilesObfuscation(quantiles=5)
    fitness_list_privacy_engine = harmonic_objective_privacy_engine.get_evaluation_result(population=population)
    assert len(fitness_list_privacy_engine) == 7

    harmonic_objective.obfuscation = QuantilesObfuscation(quantiles=5)
    fitness_list = harmonic_objective.get_evaluation_result(population=population)
    assert len(fitness_list) == 7

    assert fitness_list_privacy_engine[0].estimated_fitness == fitness_list[0].estimated_fitness == 135
    assert fitness_list_privacy_engine[1].estimated_fitness == fitness_list[1].estimated_fitness == 270
    assert fitness_list_privacy_engine[2].estimated_fitness == fitness_list[2].estimated_fitness == 0
    assert fitness_list_privacy_engine[3].estimated_fitness == fitness_list[3].estimated_fitness == 0
    assert fitness_list_privacy_engine[4].estimated_fitness == fitness_list[4].estimated_fitness == -270
    assert fitness_list_privacy_engine[5].estimated_fitness == fitness_list[5].estimated_fitness == -135
    assert fitness_list_privacy_engine[6].estimated_fitness == fitness_list[6].estimated_fitness == -270


