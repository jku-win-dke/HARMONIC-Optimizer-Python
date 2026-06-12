import multiprocessing
from datetime import datetime
from typing import Any

from .base import StatisticsBase


class OptimizationStatistics(StatisticsBase):
    populations: Any = None
    time_optimization_started: Any = None
    time_optimization_stopped: Any = None

    def __init__(self, manager, /, **data):
        super().__init__(**data)
        self.time_optimization_created = datetime.now()
        self.populations = manager.list()
        self.time_optimization_started = multiprocessing.Value('d', 0.0)
        self.time_optimization_stopped = multiprocessing.Value('d', 0.0)
