from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime

from .base import TargetTimeAssignmentBase


class TargetTimeAssignment(TargetTimeAssignmentBase):
    target_time: TargetTime
    flight: Flight
