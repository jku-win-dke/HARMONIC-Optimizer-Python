from app.models.base_mapper import BaseMapper
from app.models.fitness.mapper import FitnessMapper
from .dto import AssignmentDTO
from .obj import Assignment


class AssignmentMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Assignment) -> AssignmentDTO:
        fitness_list = [FitnessMapper.to_dto(fitness) for fitness in obj.fitness_list]

        return AssignmentDTO(
            row_ind=obj.row_ind,
            col_ind=obj.col_ind,
            fitness_list=fitness_list,
        )

    @staticmethod
    def from_dto(dto: AssignmentDTO) -> Assignment:
        return Assignment(
            row_ind=dto.row_ind,
            col_ind=dto.col_ind,
        )
