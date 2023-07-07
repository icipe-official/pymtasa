import time
import multiprocessing as mp

from afsa.parameters_set import ParametersSet, Site
from afsa.utils import Utils
from afsa.static_variables import RESULTS_DIRECTORY, TMP_DIRECTORY, NORMALIZATION_COEFFICIENTS
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
                variables in number_divisions & env_data_target
    """

    def __init__(self, parameters_set: ParametersSet):
        self.parameters_set = parameters_set
        self.formatting_analysis_period()
        self.reference = Site(self.parameters_set.longitude, self.parameters_set.latitude, self.parameters_set.env_vars,
                              self.parameters_set.env_data_ref)
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

    def compute_similarity_raster(self, start_time) -> str:
        if self.parameters_set.rotation is None:
            env_data_target_matrices = Utils.convert_raster_stack_list_into_matrix_list(
                self.parameters_set.env_data_target)
        else:
            env_data_target_matrices = self.mp_rotate_climate_data()
        print("Step 1 Over !!!!")
        print("Process Time Rotation computation : ----%.2f----" % (time.time() - start_time))
        similarity_data = self.compute_similarity_data(env_data_target_matrices)
        print("Step 2 Over !!!!")
        print("Process Time Similarity computation : ----%.2f----" % (time.time() - start_time))
        if self.parameters_set.write_file:
            return Utils.create_tiff_file_from_array(similarity_data, RESULTS_DIRECTORY,
                                                     self.parameters_set.file_name + ".tif",
                                                     self.parameters_set.env_data_target[0][0])
        return Utils.create_tiff_file_from_array(similarity_data, TMP_DIRECTORY,
                                                 self.parameters_set.file_name + ".tif",
                                                 self.parameters_set.env_data_target[0][0])

    def rotate_climate_data(self) -> list[np.ndarray]:
        rotation_matrix = self.compute_rotation_matrix()
        env_data_target_matrices = []
        for i, env_variable in enumerate(self.parameters_set.env_vars):
            index = self.parameters_set.env_vars.index(env_variable)
            env_data_target_matrix = Utils.convert_raster_stack_into_matrix(
                self.parameters_set.env_data_target[index])
            valid_values_indices = np.where(~np.isnan(rotation_matrix))[0]
            for index in valid_values_indices:
                env_data_target_matrix[index, :] = self.perform_line_rotation(rotation_matrix[index],
                                                                              env_data_target_matrix[index, :])
            env_data_target_matrices.append(env_data_target_matrix)
        return env_data_target_matrices

    def mp_rotate_climate_data(self) -> list[np.ndarray]:
        rotation_matrix = self.mp_compute_rotation_matrix()
        print("AT LEAST HERE !!!")
        env_data_target_matrices = []
        for i, env_variable in enumerate(self.parameters_set.env_vars):
            index = self.parameters_set.env_vars.index(env_variable)
            env_data_target_matrix = Utils.convert_raster_stack_into_matrix(
                self.parameters_set.env_data_target[index])
            valid_values_indices = np.where(~np.isnan(rotation_matrix))[0]
            for index in valid_values_indices:
                env_data_target_matrix[index, :] = self.perform_line_rotation(rotation_matrix[index],
                                                                              env_data_target_matrix[index, :])
            env_data_target_matrices.append(env_data_target_matrix)
        return env_data_target_matrices

    def perform_line_rotation_parallel(self, args):
        index, rotation_matrix = args
        env_data_target_matrix = Utils.convert_raster_stack_into_matrix(
            self.parameters_set.env_data_target[index])
        valid_values_indices = np.where(~np.isnan(rotation_matrix))[0]
        for i in valid_values_indices:
            env_data_target_matrix[i, :] = self.perform_line_rotation(rotation_matrix[i], env_data_target_matrix[i, :])
        return env_data_target_matrix

    def compute_rotation_matrix(self) -> np.ndarray:
        if self.parameters_set.rotation in ("prec", "tmean"):
            specific_env_data_reference_vector = np.array(self.reference.env_data[self.parameters_set.rotation])
            specific_env_data_target_paths = self.parameters_set.env_data_target[
                self.parameters_set.env_vars.index(self.parameters_set.rotation)]
            specific_env_data_target_matrix = Utils.convert_raster_stack_into_matrix(specific_env_data_target_paths)
            first_column_specific_env_data_target_matrix = specific_env_data_target_matrix[:, 0]
            rotation_data = np.array([np.nan] * len(first_column_specific_env_data_target_matrix))
            valid_values_indices = np.where(~np.isnan(first_column_specific_env_data_target_matrix))[0]
            for index in valid_values_indices:
                if not np.any(np.isnan(specific_env_data_target_matrix[index])):
                    rotation_data[index] = Utils.compute_rotation_coefficient(self.rotation_mode,
                                                                              self.parameters_set.analysis_period,
                                                                              specific_env_data_reference_vector,
                                                                              specific_env_data_target_matrix[index])
                else:
                    rotation_data[index] = 0
        else:
            specific_env_data_reference_matrix = np.array([self.reference.env_data["tmean"],
                                                           self.reference.env_data["prec"]])
            index_tmean, index_prec = self.parameters_set.env_vars.index("tmean"), self.parameters_set.env_vars.index(
                "prec")
            specific_env_data_target_matrix = Utils.convert_raster_stack_list_into_matrix([
                self.parameters_set.env_data_target[index_tmean], self.parameters_set.env_data_target[index_prec]])
            first_column_specific_env_data_target_matrix = specific_env_data_target_matrix[:, 0]
            rotation_data = np.array([np.nan] * len(first_column_specific_env_data_target_matrix))
            valid_values_indices = np.where(~np.isnan(first_column_specific_env_data_target_matrix))[0]
            num_div = self.parameters_set.number_divisions[0]
            num_div2 = 2 * num_div
            for index in valid_values_indices:
                first_row = specific_env_data_target_matrix[index, :num_div]
                last_row = specific_env_data_target_matrix[index, num_div:num_div2]
                rotation_data[index] = Utils.compute_rotation_coefficient(self.rotation_mode,
                                                                          self.parameters_set.analysis_period,
                                                                          specific_env_data_reference_matrix,
                                                                          np.array([first_row, last_row]))
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

    def mp_compute_rotation_matrix(self) -> np.ndarray:
        if self.parameters_set.rotation in ("prec", "tmean"):
            specific_env_data_reference_vector = np.array(self.reference.env_data[self.parameters_set.rotation])
            specific_env_data_target_paths = self.parameters_set.env_data_target[
                self.parameters_set.env_vars.index(self.parameters_set.rotation)]
            specific_env_data_target_matrix = Utils.convert_raster_stack_into_matrix(specific_env_data_target_paths)
            first_column_specific_env_data_target_matrix = specific_env_data_target_matrix[:, 0]
            rotation_data = np.array([np.nan] * len(first_column_specific_env_data_target_matrix))
            valid_values_indices = np.where(~np.isnan(first_column_specific_env_data_target_matrix))[0]
            for index in valid_values_indices:
                if not np.any(np.isnan(specific_env_data_target_matrix[index])):
                    rotation_data[index] = Utils.compute_rotation_coefficient(self.rotation_mode,
                                                                              self.parameters_set.analysis_period,
                                                                              specific_env_data_reference_vector,
                                                                              specific_env_data_target_matrix[index])
                else:
                    rotation_data[index] = 0
        else:
            rotation_data = self.mp_compute_absolute_rotation_matrix()
        return rotation_data

    def mp_compute_absolute_rotation_matrix(self) -> np.ndarray:
        specific_env_data_reference_matrix = np.array([self.reference.env_data["tmean"],
                                                       self.reference.env_data["prec"]])
        shared_array = mp.RawArray('d', specific_env_data_reference_matrix.flatten())
        shared_matrix = np.frombuffer(shared_array, dtype=np.float64).reshape(
            specific_env_data_reference_matrix.shape)
        index_tmean, index_prec = self.parameters_set.env_vars.index("tmean"), self.parameters_set.env_vars.index(
            "prec")
        specific_env_data_target_matrix = Utils.convert_raster_stack_list_into_matrix([
            self.parameters_set.env_data_target[index_tmean], self.parameters_set.env_data_target[index_prec]])
        rotation_data = np.array([np.nan] * len(specific_env_data_target_matrix))
        valid_values = ~np.isnan(specific_env_data_target_matrix[:, 0])
        valid_values_indices = np.where(valid_values)[0]
        valid_target_matrix = specific_env_data_target_matrix[valid_values]
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

    def perform_line_rotation(self, rotation_coefficient: int, matrix_line: np.ndarray) -> np.ndarray:
        if self.parameters_set.rotation in self.parameters_set.env_vars:
            number_divisions = self.parameters_set.number_divisions[
                self.parameters_set.env_vars.index(self.parameters_set.rotation)]
        else:
            number_divisions = self.parameters_set.number_divisions[self.parameters_set.env_vars.index("prec")]
        rotation_coefficient = int(rotation_coefficient)
        if rotation_coefficient == 0 or rotation_coefficient == number_divisions:
            return matrix_line
        else:
            return np.roll(matrix_line, rotation_coefficient)

    def compute_similarity_data(self, env_data_target_matrices: list[np.ndarray]) -> np.ndarray:
        print("BEGINNING OF THE SIMILARITY COMPUTATION")
        temp_dissimilarity_data = np.full((env_data_target_matrices[0].shape[0], len(self.parameters_set.env_vars)),
                                          np.nan)
        normalization_coefficients = [NORMALIZATION_COEFFICIENTS.get(env_var, 10) for env_var in
                                      self.parameters_set.env_vars]
        analysis_period_indices = np.array(self.parameters_set.analysis_period) - 1
        for i, env_variable in enumerate(self.parameters_set.env_vars):
            if len(self.reference.env_data[env_variable]) == 1:
                result = np.where(
                    np.isnan(env_data_target_matrices[i]) | np.isnan(self.reference.env_data[env_variable]),
                    np.nan,
                    (env_data_target_matrices[i] - self.reference.env_data[env_variable]) ** 2
                )
                result = Utils.perform_distance_normalization(np.sqrt(result), normalization_coefficients[i])
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
            else:
                first_matrix = env_data_target_matrices[i][:, analysis_period_indices]
                second_matrix = np.array(self.reference.env_data[env_variable])[analysis_period_indices]
                temp_matrix = np.square(first_matrix - second_matrix)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    result = Utils.perform_distance_normalization(np.sqrt(np.nanmean(temp_matrix, axis=1)),
                                                                  normalization_coefficients[i])
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
        combined = np.round(np.sum(temp_dissimilarity_data, axis=1), decimals=3) if \
            len(self.parameters_set.env_vars) > 1 else temp_dissimilarity_data[:, 0]
        if self.threshold_mode and self.threshold > 0:
            combined = np.where(combined < self.threshold, 0, combined)
        elif not self.threshold_mode:
            data_removal_percentage = 100 - (self.threshold * 100)
            replacement_count = int((data_removal_percentage / 100) * np.sum(~np.isnan(combined)))
            indices = np.argsort(combined, kind='mergesort', axis=None)[:replacement_count]
            combined[indices] = 0
        return combined
