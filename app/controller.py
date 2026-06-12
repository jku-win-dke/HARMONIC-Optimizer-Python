import uuid
from typing import List

from app.logger.logger_config import logger
from app.models.enums.optimization_status import Status
from app.models.enums.response import Response
from app.models.optimization.dto import *
from app.models.optimization.mapper import OptimizationMapper
from app.models.optimization.obj import Optimization


class OptimizationController:

    def __init__(self):
        self.optimizations: dict[uuid.UUID, Optimization] = {}

    def create_optimization(self, optimization_input_dto: OptimizationInputDTO) -> OptimizationOutputBaseDTO:
        """
        Creates an optimization based on an input dto and adds the optimization to the optimization dict.
        :param optimization_input_dto: OptimizationInputDTO
        :return: OptimizationBaseDTO
        """
        optimization = OptimizationMapper.from_dto(optimization_input_dto)

        self.optimizations[optimization.optimization_id] = optimization
        logger.info(f'optimization with id {optimization.optimization_id} created and added successfully')

        return OptimizationMapper.to_base_dto(optimization)

    def get_optimizations(self) -> List[OptimizationOutputBaseDTO]:
        """
        Update and return the optimizations of the optimization dict.
        :return: List of OptimizationBaseDTOs
        """
        for optimization in list(self.optimizations.values()):
            optimization.update()

        return [OptimizationMapper.to_base_dto(optimization) for optimization in self.optimizations.values()]

    def get_optimization(self, optimization_id: uuid.UUID) -> Union[Response, OptimizationOutputDTO]:
        """
        Update and return a specific optimization from the optimization dict.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputDTO | Response.OPTIMIZATION_NOT_FOUND
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        optimization.update()

        return OptimizationMapper.to_dto(optimization)

    def get_optimization_statistics(self, optimization_id: uuid.UUID) -> Union[Response, OptimizationOutputStatisticsDTO]:
        """
        Update a specific optimization from the optimization dict and return its statistics.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputStatisticsDTO | Response.OPTIMIZATION_NOT_FOUND
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        optimization.update()

        return OptimizationMapper.to_statistics_dto(optimization)

    def get_optimization_result(self, optimization_id: uuid.UUID) -> Union[Response, OptimizationOutputResultDTO]:
        """
        Update a specific optimization from the optimization dict and return its assignment.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputResultDTO | Response.OPTIMIZATION_NOT_FOUND
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        optimization.update()

        return OptimizationMapper.to_result_dto(optimization)

    def start_optimization(self, optimization_id: uuid.UUID, async_run: bool) -> Union[Response, OptimizationOutputBaseDTO]:
        """
        Starts the optimization run with the specified ID for the framework to use.
        :param optimization_id: UUID of the optimization to start the optimization run for
        :param async_run: Boolean to determine if the optimization run should be asynchronous
        :return: OptimizationBaseDTO | Responses.OPTIMIZATION_NOT_FOUND | Responses.OPTIMIZATION_ALREADY_STARTED
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        if optimization.status != Status.CREATED:
            logger.info(f'optimization with ID {optimization_id} has already been started')
            return Response.OPTIMIZATION_ALREADY_STARTED

        logger.info(f'optimization with ID {optimization_id} start run')
        optimization.run(async_run)

        if async_run:
            logger.info(f'optimization with ID {optimization_id} running')
        else:
            logger.info(f'optimization with ID {optimization_id} finished')
            optimization.update()

        return OptimizationMapper.to_base_dto(optimization)

    def abort_optimization(self, optimization_id: uuid.UUID) -> Union[Response, OptimizationOutputBaseDTO]:
        """
        Aborts the asynchronous optimization run with the specified ID using defined event flag.
        :param optimization_id: UUID of the optimization to abort
        :return: OptimizationBaseDTO | Responses.OPTIMIZATION_NOT_FOUND | Responses.OPTIMIZATION_NOT_RUNNING
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        if not optimization.abort():
            logger.info(f'optimization with ID {optimization_id} not running')
            return Response.OPTIMIZATION_NOT_RUNNING

        logger.info(f'optimization with ID {optimization_id} aborted successfully')

        return OptimizationMapper.to_base_dto(optimization)

    def delete_optimization(self, optimization_id: uuid.UUID) -> Response:
        """
        Deletes the optimization with the specified ID from the optimizations' dictionary.
        :param optimization_id: UUID of the optimization to delete
        :return: Response.OPTIMIZATION_DELETED | Response.OPTIMIZATION_NOT_FOUND | Response.OPTIMIZATION_CURRENTLY_RUNNING
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return Response.OPTIMIZATION_NOT_FOUND

        optimization.update()

        if optimization.status == Status.RUNNING:
            logger.info(f'optimization with ID {optimization_id} is currently running')
            return Response.OPTIMIZATION_CURRENTLY_RUNNING

        del self.optimizations[optimization_id]
        logger.info(f'optimization with ID {optimization_id} deleted successfully')

        return Response.OPTIMIZATION_DELETED
