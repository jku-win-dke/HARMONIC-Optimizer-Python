from typing import List

from app.models.optimization_problem.harmonic.target_time_preference.dto import TargetTimePreferenceDTO
from .base import FlightPreferencesBase


class FlightPreferencesDTO(FlightPreferencesBase):
    flight_id: str
    target_time_preferences: List[TargetTimePreferenceDTO]
