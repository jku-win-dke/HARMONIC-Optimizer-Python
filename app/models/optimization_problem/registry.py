from .ap.mapper import AssignmentProblemMapper
from .harmonic.mapper import HarmonicProblemMapper
from .problem_mapper import OptimizationProblemMapper


class OptimizationProblemMapperRegistry:
    _mapper_registry: dict[str, OptimizationProblemMapper] = {
        "harmonic": HarmonicProblemMapper,
        "ap": AssignmentProblemMapper
    }

    @staticmethod
    def get_mapper(problem_type: str) -> OptimizationProblemMapper:
        """
        Return the mapper for a particular optimization problem type.
        :param problem_type: Optimization problem type
        :return: Mapper of the optimization problem type
        """
        return OptimizationProblemMapperRegistry._mapper_registry.get(problem_type)
