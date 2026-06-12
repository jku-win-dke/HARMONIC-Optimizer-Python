import multiprocessing
import uuid
from datetime import datetime
from typing import Any, List

import numpy as np

from app.config import config
from app.models.enums.config import ApplicationMode
from app.models.enums.optimization_status import Status
from app.models.optimization_framework.obj import OptimizationFramework
from app.models.optimization_problem.obj import OptimizationProblem
from app.models.optimization_statistics.obj import OptimizationStatistics
from .base import OptimizationCreatedBase
from .custom_process.process import Process


class Optimization(OptimizationCreatedBase):
    def __init__(self, /, **data):
        super().__init__(**data)

        application_mode = config.get("application", "mode")
        if application_mode == ApplicationMode.OPS.value:
            self.optimization_id = uuid.uuid4()
        elif application_mode == ApplicationMode.DEV.value:
            self.optimization_id = uuid.UUID('00000000-0000-0000-0000-000000000001')
        else:
            raise RuntimeError('invalid configuration for application mode')

        self.manager = multiprocessing.Manager()

        self.statistics = OptimizationStatistics(self.manager)

        self.results = self.manager.list()

        self.filter_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()

    problem: OptimizationProblem
    framework: OptimizationFramework
    statistics: OptimizationStatistics = None

    manager: Any = None

    results: Any = None

    optimization_process: Any = None
    population_filter_process: Any = None
    result_filter_process: Any = None

    filter_queue: Any = None
    result_queue: Any = None


    def _shutdown_processes(self):
        if self.optimization_process:
            self.optimization_process.kill()
            self.optimization_process.join()

            self.filter_queue.put(-1)
            self.population_filter_process.join()
            self.result_filter_process.join()

    @staticmethod
    def population_filter_process_method(filter_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue,
                                         populations: List) -> None:
        i = filter_queue.get(block=True)
        while i > -1:
            population = populations[i]

            # only keep pareto optimal solutions of a population
            population.solutions = population.get_pareto_optimal_solutions()
            population.filtered = True

            populations[i] = population
            result_queue.put(i)

            i = filter_queue.get(block=True)
        result_queue.put(-1)

    @staticmethod
    def result_filter_process_method(result_queue: multiprocessing.Queue, populations: List, time_optimization_stopped: multiprocessing.Value, results: List,
                                     result_size: int, problem: OptimizationProblem) -> None:
        i = result_queue.get(block=True)
        while i > -1:
            temp_population = populations[i]
            temp_population.solutions.extend(results)

            solutions = temp_population.get_pareto_optimal_solutions()

            if result_size is None:
                results[:] = solutions

            else:
                current_size = len(solutions)

                if current_size <= result_size:
                    results[:] = solutions

                else:
                    # calculate crowding distance (based on nsga-ii) as tiebreaker
                    distances = np.zeros(current_size)

                    for objective in problem.objectives:

                        fitness_values = [
                            next(f.get_estimated_or_actual_fitness()
                                 for f in solution.fitness_list
                                 if f.objective_id == objective.objective_id)
                            for solution in solutions
                        ]

                        min_fitness = np.min(fitness_values)
                        max_fitness = np.max(fitness_values)

                        indices = np.argsort(fitness_values)

                        distances[indices[0]] = np.inf
                        distances[indices[-1]] = np.inf

                        for i in range(1, current_size - 1):
                            prev_fitness = fitness_values[indices[i - 1]]
                            next_fitness = fitness_values[indices[i + 1]]

                            if max_fitness != min_fitness:
                                distances[indices[i]] += (next_fitness - prev_fitness) / (max_fitness - min_fitness)

                    indices = sorted(range(len(distances)), key=lambda j: distances[j], reverse=True)

                    temp_results = []
                    for i in range(result_size):
                        temp_results.append(solutions[indices[i]])

                    results[:] = temp_results

            i = result_queue.get(block=True)

        time_optimization_stopped.value = datetime.now().timestamp()

    def run(self, async_run: bool) -> bool:
        """
        Creates a new process for the optimization run and starts it.
        :param async_run: Boolean to determine if the optimization run should be asynchronous or not.
        :return: Indicates if the optimization run was started successfully.
        """
        self.statistics.time_optimization_started.value = datetime.now().timestamp()
        try:
            self.optimization_process = Process(target=self.framework.execute,
                                                args=(self.problem,
                                                      self.statistics.populations,
                                                      self.filter_queue),
                                                daemon=True)
            self.optimization_process.start()

            self.population_filter_process = Process(target=self.population_filter_process_method,
                                                     args=(self.filter_queue,
                                                           self.result_queue,
                                                           self.statistics.populations),
                                                     daemon=True)

            self.population_filter_process.start()

            self.result_filter_process = Process(target=self.result_filter_process_method,
                                                 args=(self.result_queue,
                                                       self.statistics.populations,
                                                       self.statistics.time_optimization_stopped,
                                                       self.results,
                                                       self.result_size,
                                                       self.problem),
                                                 daemon=True)

            self.result_filter_process.start()

            self.status = Status.RUNNING

            if not async_run:
                self.optimization_process.join()
                self.population_filter_process.join()
                self.result_filter_process.join()

            return True

        except Exception as e:
            self.status = Status.FAILED
            self._shutdown_processes()

            return False

    def abort(self) -> bool:
        """
        Aborts the optimization and calls for an update of the optimization
        :return: Indicates if the optimization was aborted successfully.
        """
        if (self.optimization_process is None) or (not self.optimization_process.is_alive()):
            return False

        self._shutdown_processes()
        self.update()
        self.status = Status.ABORTED
        return True

    def update(self) -> None:
        """
        Updates the attributes of the optimization and the result if the optimization is running or finished
        Only pareto optimal solutions are in the optimization result and populations of the statistics
        :return: None
        """
        # in the case of exception, do not provide a result
        if self.optimization_process and self.optimization_process.exception:
            self.status = Status.FAILED

            self._shutdown_processes()
            self.results = []

        # check if update has already been called
        if self.status != Status.RUNNING:
            return

        result_filtering_finished = False
        if self.results:
            if not self.result_filter_process.is_alive():
                result_filtering_finished = True
            self.problem.update_result(self.results)

        if not self.optimization_process.is_alive() and not self.population_filter_process.is_alive() and result_filtering_finished:
            self.status = Status.FINISHED
            self.results = []
