from abc import ABC, abstractmethod
from typing import Any


class BaseMapper(ABC):

    @staticmethod
    @abstractmethod
    def to_dto(**kwargs) -> Any:
        """
        Map a domain object to a data transfer object.
        :param kwargs: The domain object.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dto(**kwargs) -> Any:
        """
        Map a data transfer object to a domain object.
        :param kwargs: The data transfer object and additional attributes, if required.
        """
        pass
