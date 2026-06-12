from typing import List

from app.models.base_mapper import BaseMapper
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime
from app.models.optimization_problem.harmonic.target_time_preference.dto import TargetTimePreferenceDTO
from app.models.optimization_problem.harmonic.target_time_preference.obj import TargetTimePreference


class TargetTimePreferenceMapper(BaseMapper):

    @staticmethod
    def to_dto(obj: TargetTimePreference) -> TargetTimePreferenceDTO:
        return TargetTimePreferenceDTO(
            target_time_id=obj.target_time.target_time_id,
            weight=obj.weight,
        )

    @staticmethod
    def from_dto(dto: TargetTimePreferenceDTO, target_times: List[TargetTime]) -> TargetTimePreference:

        target_time_ref = None
        for target_time in target_times:
            if target_time.target_time_id == dto.target_time_id:
                target_time_ref = target_time

        return TargetTimePreference(
            target_time=target_time_ref,
            weight=dto.weight,
        )
