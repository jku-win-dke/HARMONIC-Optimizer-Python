from .base import TargetTimeAssignmentBase


class TargetTimeAssignmentDTO(TargetTimeAssignmentBase):
    target_time_id: str
    flight_id: str
