from enum import Enum

from fastapi import status


class Response(Enum):
    OPTIMIZATION_NOT_FOUND = (status.HTTP_404_NOT_FOUND, 'Optimization with ID {optimization_id} not found.')
    OPTIMIZATION_ALREADY_STARTED = (status.HTTP_409_CONFLICT, 'Optimization with ID {optimization_id} already started.')
    OPTIMIZATION_NOT_RUNNING = (status.HTTP_409_CONFLICT, 'Optimization with ID {optimization_id} is not running.')
    OPTIMIZATION_CURRENTLY_RUNNING = (status.HTTP_409_CONFLICT, 'Optimization with ID {optimization_id} is currently running.')
    OPTIMIZATION_DELETED = (status.HTTP_200_OK, 'Optimization with ID {optimization_id} deleted successfully.')


    def format_message(self, **kwargs):
        return self.value[1].format(**kwargs)
