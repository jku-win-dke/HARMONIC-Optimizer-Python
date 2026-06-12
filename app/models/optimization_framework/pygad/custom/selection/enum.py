import enum

from app.models.optimization_framework.pygad.custom.selection.npga import npga_selection
from app.models.optimization_framework.pygad.custom.selection.nsga2_modified import nsga2_selection_modified
from app.models.optimization_framework.pygad.custom.selection.spea2 import spea2_selection
from app.models.optimization_framework.pygad.custom.selection.tournament_ko import tournament_ko_selection
from app.models.optimization_framework.pygad.custom.selection.tournament_front import tournament_front_selection


class CustomSelectionOperators(enum.Enum):
    NPGA = ('npga', npga_selection)

    NSGA2_MODIFIED = ('nsga2_modified', nsga2_selection_modified)

    SPEA2 = ('spea2', spea2_selection)

    TOURNAMENT_KO = ('tournament_ko', tournament_ko_selection)

    TOURNAMENT_FRONT = ('tournament_front', tournament_front_selection)
