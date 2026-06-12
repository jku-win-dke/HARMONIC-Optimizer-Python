from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_preference.base import TargetTimePreferenceBase


class TargetTimePreference(TargetTimePreferenceBase):
    target_time: TargetTime
