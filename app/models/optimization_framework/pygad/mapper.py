from app.models.base_mapper import BaseMapper

from .dto import PygadFrameworkDTO
from .obj import PygadFramework


class PygadFrameworkMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: PygadFramework) -> PygadFrameworkDTO:
        return PygadFrameworkDTO(
            keep_genes_probability=obj.keep_genes_probability,
            archive_size=obj.archive_size,
            comparison_sample_size=obj.comparison_sample_size,
            niche_radius=obj.niche_radius,
            num_generations=obj.num_generations,
            num_parents_mating=obj.num_parents_mating,
            sol_per_pop=obj.sol_per_pop,
            init_range_low=obj.init_range_low,
            init_range_high=obj.init_range_high,
            parent_selection_type=obj.parent_selection_type,
            keep_parents=obj.keep_parents,
            keep_elitism=obj.keep_elitism,
            K_tournament=obj.K_tournament,
            crossover_type=obj.crossover_type,
            crossover_probability=obj.crossover_probability,
            mutation_type=obj.mutation_type,
            mutation_probability=obj.mutation_probability,
            mutation_by_replacement=obj.mutation_by_replacement,
            mutation_percent_genes=obj.mutation_percent_genes,
            mutation_num_genes=obj.mutation_num_genes,
            random_mutation_min_val=obj.random_mutation_min_val,
            random_mutation_max_val=obj.random_mutation_max_val,
            save_best_solutions=obj.save_best_solutions,
            save_solutions=obj.save_solutions,
            stop_criteria=obj.stop_criteria,
            parallel_processing=obj.parallel_processing,
            random_seed=obj.random_seed,
        )

    @staticmethod
    def from_dto(dto: PygadFrameworkDTO) -> PygadFramework:
        return PygadFramework(
            keep_genes_probability=dto.keep_genes_probability,
            archive_size=dto.archive_size,
            comparison_sample_size=dto.comparison_sample_size,
            niche_radius=dto.niche_radius,
            num_generations=dto.num_generations,
            num_parents_mating=dto.num_parents_mating,
            sol_per_pop=dto.sol_per_pop,
            init_range_low=dto.init_range_low,
            init_range_high=dto.init_range_high,
            parent_selection_type=dto.parent_selection_type,
            keep_parents=dto.keep_parents,
            keep_elitism=dto.keep_elitism,
            K_tournament=dto.K_tournament,
            crossover_type=dto.crossover_type,
            crossover_probability=dto.crossover_probability,
            mutation_type=dto.mutation_type,
            mutation_probability=dto.mutation_probability,
            mutation_by_replacement=dto.mutation_by_replacement,
            mutation_percent_genes=dto.mutation_percent_genes,
            mutation_num_genes=dto.mutation_num_genes,
            random_mutation_min_val=dto.random_mutation_min_val,
            random_mutation_max_val=dto.random_mutation_max_val,
            save_best_solutions=dto.save_best_solutions,
            save_solutions=dto.save_solutions,
            stop_criteria=dto.stop_criteria,
            parallel_processing=dto.parallel_processing,
            random_seed=dto.random_seed,
        )
