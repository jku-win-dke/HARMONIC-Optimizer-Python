from app.models.base_mapper import BaseMapper
from app.models.optimization_framework.registry import OptimizationFrameworkMapperRegistry
from app.models.optimization_problem.registry import OptimizationProblemMapperRegistry
from app.models.optimization_statistics.mapper import OptimizationStatisticsMapper
from .dto import OptimizationInputDTO, OptimizationOutputDTO, OptimizationOutputBaseDTO, \
    OptimizationOutputStatisticsDTO, OptimizationOutputResultDTO
from .obj import Optimization


class OptimizationMapper(BaseMapper):

    @staticmethod
    def to_dto(obj: Optimization) -> OptimizationOutputDTO:
        statistics = OptimizationStatisticsMapper.to_dto(obj.statistics)

        problem_mapper = OptimizationProblemMapperRegistry.get_mapper(obj.problem.problem_type)
        problem = problem_mapper.to_dto(obj=obj.problem)

        framework_mapper = OptimizationFrameworkMapperRegistry.get_mapper(obj.framework.framework_type)
        framework = framework_mapper.to_dto(obj=obj.framework)

        return OptimizationOutputDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            result_size=obj.result_size,
            statistics=statistics,
            problem=problem,
            framework=framework
        )

    @staticmethod
    def to_base_dto(obj: Optimization) -> OptimizationOutputBaseDTO:
        return OptimizationOutputBaseDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            result_size=obj.result_size,
        )

    @staticmethod
    def to_statistics_dto(obj: Optimization) -> OptimizationOutputStatisticsDTO:
        statistics_dto = OptimizationStatisticsMapper.to_dto(obj.statistics)

        return OptimizationOutputStatisticsDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            result_size=obj.result_size,
            statistics=statistics_dto
        )

    @staticmethod
    def to_result_dto(obj: Optimization) -> OptimizationOutputResultDTO:
        problem_mapper = OptimizationProblemMapperRegistry.get_mapper(obj.problem.problem_type)
        problem_dto = problem_mapper.to_result_dto(obj=obj.problem)

        return OptimizationOutputResultDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            result_size=obj.result_size,
            problem=problem_dto
        )

    @staticmethod
    def from_dto(dto: OptimizationInputDTO) -> Optimization:
        problem_mapper = OptimizationProblemMapperRegistry.get_mapper(dto.problem.problem_type)
        problem = problem_mapper.from_dto(dto=dto.problem)

        framework_mapper = OptimizationFrameworkMapperRegistry.get_mapper(dto.framework.framework_type)
        framework = framework_mapper.from_dto(dto=dto.framework)

        return Optimization(
            result_size=dto.result_size,
            problem=problem,
            framework=framework,
        )
