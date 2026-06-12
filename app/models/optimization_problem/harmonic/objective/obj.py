import json
from typing import List, Any

import numpy as np
import requests
from requests.exceptions import ConnectionError

from app.models.fitness.obj import Fitness
from app.models.optimization_objective.obj import OptimizationObjective
from app.models.optimization_problem.harmonic.flight.obj import Flight
from app.models.optimization_problem.harmonic.flight_preferences.obj import FlightPreferences
from app.models.optimization_problem.harmonic.objective.base import HarmonicObjectiveBase
from app.models.optimization_problem.harmonic.target_time.obj import TargetTime


class HarmonicObjective(HarmonicObjectiveBase, OptimizationObjective):
    flight_preferences: List[FlightPreferences]
    matrix: Any = None

    def _get_fitness(self, encoding: List[int]) -> Fitness:
        fitness = 0

        for i in range(len(encoding)):
            if encoding[i] > -1:
                fitness += self.matrix[i][encoding[i]]

        return Fitness(objective_id=self.objective_id, actual_fitness=fitness)

    def init_evaluation_setup(self, flights: List[Flight], target_times: List[TargetTime]) -> None:
        """
        Convert the preference into a 2D array based on the situational representation.
        If there are more flights than target times, the number of flights is used as the first dimension and the number of target times as the second dimension.
        Vice versa if there are more target times than flights.
        @param flights: ...
        @param target_times: ...
        @return: 2D array containing the weights of the preference.
        """
        if isinstance(self.flight_preferences[0].target_time_preferences[0].weight, int):
            # Get the flight and target time IDs
            flight_ids = [flight.flight_id for flight in flights]
            target_time_ids = [target_time.target_time_id for target_time in target_times]

            # Create a 2D array with the shape of the flights and target times
            self.matrix = np.zeros((len(flights), len(target_times)), dtype=np.float64)

            for flight_preference in self.flight_preferences:
                flight_index = flight_ids.index(flight_preference.flight.flight_id)
                for target_time_preference in flight_preference.target_time_preferences:
                    target_time_index = target_time_ids.index(target_time_preference.target_time.target_time_id)
                    self.matrix[flight_index][target_time_index] = target_time_preference.weight

        # Transpose the matrix if the number of target times is greater than the number of flights
        if len(target_times) > len(flights):
            self.matrix = self.matrix.T

        if self.privacy_engine:
            try:
                decoder = json.JSONDecoder()

                # If the privacy engine is used for an imbalanced problem, a dummy column is added to the matrix
                # This column is later used to indicate no assignment
                if self.matrix.shape[0] != self.matrix.shape[1]:
                    dummy_column = np.zeros((self.matrix.shape[0], 1), dtype=np.float64)
                    self.matrix = np.column_stack((self.matrix, dummy_column))

                # Encode the weights and initialize a secret-shared session
                request_encode = requests.put(f'{self.encoding_url}', json=self.matrix.tolist())

                if request_encode.status_code == 200:
                    encoded_weights = decoder.decode(request_encode.content.decode())
                    _ = requests.put(f'{self.privacy_engine}/sessionSecret', json={'mapping': {}, 'weights': encoded_weights})
                else:
                    raise RuntimeError(f'Encoder is not available and objective {self.objective_id} cannot be initialized')

            except ConnectionError as e:
                raise RuntimeError(f'Encoder is not available and objective {self.objective_id} cannot be initialized')
