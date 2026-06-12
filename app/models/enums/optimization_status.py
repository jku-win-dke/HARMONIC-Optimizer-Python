from enum import Enum


class Status(Enum):
    CREATED = 'CREATED'
    RUNNING = 'RUNNING'
    ABORTED = 'ABORTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'
