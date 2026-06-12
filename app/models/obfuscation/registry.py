from app.models.base_mapper import BaseMapper

from .above.mapper import AboveObfuscationMapper
from .buckets.mapper import BucketsObfuscationMapper
from .order.mapper import OrderObfuscationMapper
from .quantiles.mapper import QuantilesObfuscationMapper
from .top.mapper import TopObfuscationMapper


class ObfuscationMapperRegistry:
    _mapper_registry: dict[str, BaseMapper] = {
        "order": OrderObfuscationMapper,
        "top": TopObfuscationMapper,
        "above": AboveObfuscationMapper,
        "quantiles": QuantilesObfuscationMapper,
        "buckets": BucketsObfuscationMapper,
    }

    @staticmethod
    def get_mapper(obfuscation_type: str) -> BaseMapper:
        return ObfuscationMapperRegistry._mapper_registry.get(obfuscation_type)
