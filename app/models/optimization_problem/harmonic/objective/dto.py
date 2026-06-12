from typing import List

from app.models.optimization_objective.dto import OptimizationObjectiveDTO
from app.models.optimization_problem.harmonic.flight_preferences.dto import FlightPreferencesDTO
from app.models.optimization_problem.harmonic.objective.base import HarmonicObjectiveBase


class HarmonicObjectiveDTO(HarmonicObjectiveBase, OptimizationObjectiveDTO):
    flight_preferences: List[FlightPreferencesDTO]
