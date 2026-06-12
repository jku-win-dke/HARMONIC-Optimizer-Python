from typing import List

from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.target_time_preference.obj import TargetTimePreference
from .base import FlightPreferencesBase


class FlightPreferences(FlightPreferencesBase):
    flight: Flight
    target_time_preferences: List[TargetTimePreference]
