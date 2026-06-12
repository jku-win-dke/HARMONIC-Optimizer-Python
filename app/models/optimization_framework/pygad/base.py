from abc import ABC
from typing import Literal, Optional, Union, List, Tuple

from pydantic import BaseModel, model_validator

from app.models.optimization_framework.pygad.custom.crossover.enum import CustomCrossoverOperators
from app.models.optimization_framework.pygad.custom.mutation.enum import CustomMutationOperators
from app.models.optimization_framework.pygad.custom.selection.enum import CustomSelectionOperators


class PygadFrameworkBase(ABC, BaseModel):
    framework_type: Literal["pygad"] = "pygad"
    # UOX
    keep_genes_probability: float = 0.5
    # SPEA-2
    _archive = []
    archive_size: Optional[int] = None
    # NPGA
    comparison_sample_size: Optional[int] = None
    niche_radius: Optional[float] = None

    num_generations: int
    num_parents_mating: int
    sol_per_pop: int
    init_range_low: int = -4
    init_range_high: int = 4
    parent_selection_type: Optional[Literal[
        'sss', 'rws', 'sus', 'rank', 'random', 'tournament', 'tournament_nsga2', 'nsga2', 'nsga2_modified', 'spea2', 'tournament_ko', 'tournament_front']] = None
    keep_parents: int = 0
    keep_elitism: int = 0
    K_tournament: int = 3
    crossover_type: Optional[Literal['single_point', 'two_points', 'uniform', 'scattered', 'pmx', 'uox']] = None
    crossover_probability: Optional[float] = None
    mutation_type: Optional[Literal['random', 'swap', 'inversion', 'scramble', 'adaptive', 'shift1', 'shift2']] = None
    mutation_probability: Optional[float] = None
    mutation_by_replacement: bool = False
    mutation_percent_genes: int = 10
    mutation_num_genes: Optional[int] = None
    random_mutation_min_val: float = -1.0
    random_mutation_max_val: float = 1.0
    save_best_solutions: bool = False
    save_solutions: bool = False
    stop_criteria: Optional[str] = None
    parallel_processing: Optional[Union[int, List[Union[str, int]], Tuple[Union[str, int], ...]]] = None
    random_seed: Optional[int] = None

    @property
    def mutation_type_mapping(self):
        if isinstance(self.mutation_type, str):

            for mutation in CustomMutationOperators:
                if self.mutation_type == mutation.value[0]:
                    return mutation.value[1]

        return self.mutation_type

    @property
    def crossover_type_mapping(self):
        if isinstance(self.crossover_type, str):

            # UOX
            if self.crossover_type == CustomCrossoverOperators.UOX.value[0]:
                if self.keep_genes_probability is None:
                    raise ValueError("keep_genes_probability is None")
                return lambda parents, offspring_size, ga_instance: (
                    CustomCrossoverOperators.UOX.value[1](parents, offspring_size, ga_instance,
                                                          self.keep_genes_probability))

            # other custom crossover operators
            for crossover in CustomCrossoverOperators:
                if self.crossover_type == crossover.value[0]:
                    return crossover.value[1]

        return self.crossover_type

    @property
    def parent_selection_mapping(self):
        if isinstance(self.parent_selection_type, str):

            # SPEA 2
            if self.parent_selection_type == CustomSelectionOperators.SPEA2.value[0]:
                if self.archive_size is None:
                    raise ValueError("archive_size is None")

                if self.keep_parents > 0:
                    raise ValueError('keep_parents must be 0 for SPEA2 selection operator')

                return lambda fitness, num_parents, ga_instance: (
                    CustomSelectionOperators.SPEA2.value[1](fitness, num_parents, ga_instance, self._archive,
                                                            self.archive_size))

            # NPGA
            elif self.parent_selection_type == CustomSelectionOperators.NPGA.value[0]:
                if self.comparison_sample_size is None:
                    raise ValueError("comparison_sample_size is None")
                if self.niche_radius is None:
                    raise ValueError("niche_radius is None")

                return lambda fitness, num_parents, ga_instance: (
                    CustomSelectionOperators.NPGA.value[1](fitness, num_parents, ga_instance,
                                                           self.comparison_sample_size, self.niche_radius))

            # other selection operators
            for selection in CustomSelectionOperators:
                if self.parent_selection_type == selection.value[0]:
                    return selection.value[1]

        return self.parent_selection_type

    @model_validator(mode='after')
    def validate_property_mappings(self):
        _ = self.mutation_type_mapping
        _ = self.crossover_type_mapping
        _ = self.parent_selection_mapping
        return self
