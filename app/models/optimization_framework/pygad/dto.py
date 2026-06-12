from app.models.optimization_framework.dto import OptimizationFrameworkDTO

from .base import PygadFrameworkBase


class PygadFrameworkDTO(PygadFrameworkBase, OptimizationFrameworkDTO):
    pass
