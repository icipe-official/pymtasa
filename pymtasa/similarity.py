import time
import multiprocessing as mp
import gc

from pymtasa.parameters_set import Site, ParametersSet
from pymtasa.utils import Utils
from pymtasa.static_variables import RESULTS_DIRECTORY, NORMALIZATION_COEFFICIENTS
import warnings
import numpy as np


class Similarity:
    """
        parameters_set (ParametersSet) : set of parameters used to compute the agro ecology similarity
        reference (Site) : site that will be used as reference to evaluate the agro ecology similarity
        threshold (float) : value between 0-1. Only sites with a climatic similarity above this threshold will be
                saved and displayed.
        absolute_mode (bool) : specify if the threshold is an absolute or relative value. True for absolute value, False
            for relative value.

        Note :  We assume that the position of the variables in env_vars follows the same order as the position of the
                variables in number_divisions & data_target
    """

    def __init__(self, parameters_set: ParametersSet):
        self.parameters_set = parameters_set
        self.formatting_analysis_period()
        self.reference = Site(self.parameters_set.measurement_vars, self.parameters_set.ref_data)
        self.threshold = parameters_set.threshold
        self.rotation_mode = parameters_set.rotation_mode
        self.threshold_mode = parameters_set.threshold_mode

    def formatting_analysis_period(self):
        analysis_period = self.parameters_set.analysis_period
        if len(analysis_period) == 1:
            tmp_result = analysis_period
        elif len(analysis_period) == 2 and analysis_period[0] > analysis_period[1]:
            # E.g : [11, 2] must become [11, 12, 1, 2]
            tmp_result = list(range(analysis_period[0], 13)) + list(range(1, analysis_period[1] + 1))
        elif len(analysis_period) == 2 and analysis_period[0] < analysis_period[1]:
            # E.g : [3, 5] must become [3, 4, 5]
            tmp_result = list(range(analysis_period[0], analysis_period[1] + 1))
        elif len(analysis_period) == 4 and analysis_period[0] > analysis_period[1]:
            # E.g : [11, 3, 6, 8] must become [11, 12] + [1, 2, 3] + [6, 7, 8] = [11, 12, 1, 2, 3, 6, 7, 8]
            tmp_result = list(range(analysis_period[0], 13)) + list(range(1, analysis_period[1] + 1)) + \
                         list(range(analysis_period[2], analysis_period[3] + 1))
        elif len(analysis_period) == 4 and analysis_period[2] > analysis_period[3]:
            # E.g : [6, 8, 11, 2] must become [6, 7, 8] + [11, 12] + [1, 2] = [6, 7, 8, 11, 12, 1, 2]
            tmp_result = list(range(analysis_period[0], analysis_period[1] + 1)) + \
                         list(range(analysis_period[2], 13)) + list(range(1, analysis_period[3] + 1))
        else:
            # E.g : [1, 3, 6, 8] must become [1, 2, 3] + [6, 7, 8] = [1, 2, 3, 6, 7, 8]
            tmp_result = list(range(analysis_period[0], analysis_period[1] + 1)) + \
                         list(range(analysis_period[2], analysis_period[3] + 1))

        self.parameters_set.analysis_period = Utils.remove_duplicates(tmp_result)

    def compute_similarity_matrix(self, start_time) -> str:
        if self.parameters_set.rotation_variables is None or len(self.parameters_set.rotation_variables) == 0:
            target_data_matrices = Utils.convert_time_series_dataset_into_matrix_list(
                self.parameters_set.target_dataset, self.parameters_set.headers_indices)
            rotation_array = np.full((target_data_matrices[0].shape[0],), np.nan)
        else:
            rotation_array, target_data_matrices = self.mp_rotate_climate_data()

        print("Step 1 Over !!!!")
        print("Process Time Rotation computation : ----%.2f----" % (time.time() - start_time))
        similarity_data = self.compute_similarity_data(target_data_matrices)
        del target_data_matrices
        gc.collect()
        print("Step 2 Over !!!!")
        print("Process Time Similarity computation : ----%.2f----" % (time.time() - start_time))
        ids_array = Utils.csv_into_matrix(self.parameters_set.target_dataset[0], [0])
        similarity_index_matrix = np.column_stack((ids_array, rotation_array, similarity_data))
        similarity_index_matrix = similarity_index_matrix[(-similarity_index_matrix[:, 2]).argsort()]
        if self.parameters_set.write_file:
            headers = ['ID', 'Rotation coefficient', 'Similarity index']
            return Utils.create_csv_file_from_matrix(similarity_index_matrix, RESULTS_DIRECTORY,
                                                     self.parameters_set.file_name + ".csv", headers)
        return similarity_index_matrix

    def mp_rotate_climate_data(self) -> (np.ndarray, list[np.ndarray]):
        rotation_matrix = self.mp_compute_rotation_matrix()
        target_data_matrices = []
        for i, measurement_var in enumerate(self.parameters_set.measurement_vars):
            index = self.parameters_set.measurement_vars.index(measurement_var)
            target_data_matrix = Utils.csv_into_matrix(
                self.parameters_set.target_dataset[index], self.parameters_set.headers_indices[i])
            valid_values_indices = np.where(~np.isnan(rotation_matrix))[0]
            for index in valid_values_indices:
                target_data_matrix[index, :] = self.perform_line_rotation(int(rotation_matrix[index]),
                                                                          target_data_matrix[index, :])
            target_data_matrices.append(target_data_matrix)
        return rotation_matrix, target_data_matrices

    def mp_compute_rotation_matrix(self) -> np.ndarray:
        if len(self.parameters_set.rotation_variables) == 1:
            specific_reference_data_vector = np.array(self.reference.data[self.parameters_set.rotation_variables[0]])
            specific_target_data_paths = self.parameters_set.target_dataset[0]
            specific_target_data_matrix = Utils.csv_into_matrix(specific_target_data_paths,
                                                                self.parameters_set.headers_indices[0])
            first_column_specific_target_data_matrix = specific_target_data_matrix[:, 0]
            rotation_data = np.array([np.nan] * len(first_column_specific_target_data_matrix))
            valid_values_indices = np.where(~np.isnan(first_column_specific_target_data_matrix))[0]
            for index in valid_values_indices:
                if not np.any(np.isnan(first_column_specific_target_data_matrix[index])):
                    rotation_data[index] = Utils.compute_rotation_coefficient(self.rotation_mode,
                                                                              self.parameters_set.analysis_period,
                                                                              specific_reference_data_vector,
                                                                              specific_target_data_matrix[
                                                                                  index])
                else:
                    rotation_data[index] = 0
        else:
            rotation_data = self.mp_compute_absolute_rotation_matrix()
        return rotation_data

    def mp_compute_absolute_rotation_matrix(self) -> np.ndarray:
        specific_reference_data_matrix = np.array([self.reference.data[i] for i in
                                                   self.parameters_set.rotation_variables])
        shared_array = mp.RawArray('d', specific_reference_data_matrix.flatten())
        shared_matrix = np.frombuffer(shared_array, dtype=np.float64).reshape(
            specific_reference_data_matrix.shape)
        rotation_variables_indices = [self.parameters_set.measurement_vars.index(i) for i in
                                      self.parameters_set.rotation_variables]
        rotation_variables_headers_indices = [self.parameters_set.headers_indices[i] for i in
                                              rotation_variables_indices]
        file_paths_list = [self.parameters_set.target_dataset[index] for index in rotation_variables_indices]
        specific_target_data_matrix = Utils.convert_time_series_dataset_into_matrix(file_paths_list,
                                                                                    rotation_variables_headers_indices)
        rotation_data = np.array([np.nan] * len(specific_target_data_matrix))
        valid_values = ~np.isnan(specific_target_data_matrix[:, 0])
        valid_values_indices = np.where(valid_values)[0]
        valid_target_matrix = specific_target_data_matrix[valid_values]
        num_div = self.parameters_set.number_divisions[0]

        pool = mp.Pool()
        args = [(valid_values_indices[i], valid_target_matrix[i], num_div, shared_matrix)
                for i in range(len(valid_values_indices))]
        results = pool.map(self.compute_rotation_coefficient_parallel, args)
        for index, rotation_coefficient in results:
            rotation_data[index] = rotation_coefficient
        pool.close()
        pool.join()
        return rotation_data

    def compute_rotation_coefficient_parallel(self, arguments):
        i, target_row, div, shared_reference_matrix = arguments
        first_row = target_row[:div]
        last_row = target_row[div:(div * 2)]
        coefficient = Utils.compute_rotation_coefficient(self.rotation_mode,
                                                         self.parameters_set.analysis_period,
                                                         shared_reference_matrix,
                                                         np.array([first_row, last_row]))
        return i, coefficient

    def perform_line_rotation(self, rotation_coefficient: int, matrix_line: np.ndarray) -> np.ndarray:
        if (len(self.parameters_set.rotation_variables) == 1 and self.parameters_set.rotation_variables in
                self.parameters_set.measurement_vars):
            number_divisions = self.parameters_set.number_divisions[
                self.parameters_set.measurement_vars.index(self.parameters_set.rotation_variables)]
        else:
            number_divisions = self.parameters_set.number_divisions[self.parameters_set.measurement_vars.index(
                self.parameters_set.rotation_variables[0])]
        if rotation_coefficient == 0 or rotation_coefficient == number_divisions:
            return matrix_line
        else:
            return np.concatenate((matrix_line[rotation_coefficient:], matrix_line[:rotation_coefficient]))

    def compute_similarity_data(self, target_data_matrices: list[np.ndarray]) -> np.ndarray:
        temp_dissimilarity_data = np.full((target_data_matrices[0].shape[0],
                                           len(self.parameters_set.measurement_vars)), np.nan)
        normalization_coefficients = [NORMALIZATION_COEFFICIENTS.get(measurement_var, 10) for measurement_var in
                                      self.parameters_set.measurement_vars]
        analysis_period_indices = np.array(self.parameters_set.analysis_period) - 1
        for i, measurement_var in enumerate(self.parameters_set.measurement_vars):
            if len(self.reference.data[measurement_var]) == 1:
                result = np.where(
                    np.isnan(target_data_matrices[i]) | np.isnan(self.reference.data[measurement_var]),
                    np.nan,
                    (target_data_matrices[i] - self.reference.data[measurement_var]) ** 2
                )
                result = Utils.perform_distance_normalization(np.sqrt(result), normalization_coefficients[i])
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
            else:
                first_matrix = target_data_matrices[i][:, analysis_period_indices]
                second_matrix = np.array(self.reference.data[measurement_var])[analysis_period_indices]
                temp_matrix = np.square(first_matrix - second_matrix)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    result = Utils.perform_distance_normalization(np.sqrt(np.nanmean(temp_matrix, axis=1)),
                                                                  normalization_coefficients[i])
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
        combined = np.round(np.sum(temp_dissimilarity_data, axis=1), decimals=3) if \
            len(self.parameters_set.measurement_vars) > 1 else temp_dissimilarity_data[:, 0]
        if self.threshold_mode and self.threshold > 0:
            combined = np.where(combined < self.threshold, 0, combined)
        elif not self.threshold_mode:
            data_removal_percentage = 100 - (self.threshold * 100)
            replacement_count = int((data_removal_percentage / 100) * np.sum(~np.isnan(combined)))
            indices = np.argsort(combined, kind='mergesort', axis=None)[:replacement_count]
            combined[indices] = 0
        return combined
