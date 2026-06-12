from datetime import datetime

from app.models.base_mapper import BaseMapper
from app.models.population.mapper import PopulationMapper
from .dto import StatisticsDTO
from .obj import OptimizationStatistics


class OptimizationStatisticsMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: OptimizationStatistics) -> StatisticsDTO:
        populations = [
            PopulationMapper.to_dto(population)
            for population in obj.populations
            if population.filtered == True]
        
        time_optimization_started = None
        if obj.time_optimization_started.value > 0.0:
            time_optimization_started=datetime.fromtimestamp(obj.time_optimization_started.value)
        
        time_optimization_stopped = None
        if obj.time_optimization_stopped.value > 0.0:
            time_optimization_stopped=datetime.fromtimestamp(obj.time_optimization_stopped.value)  

        return StatisticsDTO(
            time_optimization_created=obj.time_optimization_created,
            time_optimization_started=time_optimization_started,
            time_optimization_stopped=time_optimization_stopped,
            populations=populations
        )

    @staticmethod
    def from_dto(optimization_statistics_dto):
        raise Exception("Not implemented")
