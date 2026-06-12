from datetime import datetime
from typing import List, Optional

from app.models.population.dto import PopulationDTO
from .base import StatisticsBase


class StatisticsDTO(StatisticsBase):
    time_optimization_started: Optional[datetime] = None
    time_optimization_stopped: Optional[datetime] = None
    populations: List[PopulationDTO] = []
