from analogues.parameters_set import ParametersSet, Site
from analogues.utils import Utils
from analogues.static_variables import RESULTS_DIRECTORY, TMP_DIRECTORY
import warnings
import numpy as np


class Similarity:
    """
        parameters_set (ParametersSet) : set of parameters used to compute the agro ecology similarity

        Note :  We assume that the position of the variables in env_vars follows the same order as the position of the
                variables in number_divisions & env_data_target
    """

    def __init__(self, parameters_set: ParametersSet):
        self.parameters_set = parameters_set

    def compute_similarity_raster(self) -> str:
        reference = Site(self.parameters_set.longitude, self.parameters_set.latitude, self.parameters_set.env_vars,
                         self.parameters_set.env_data_ref)
        if self.parameters_set.rotation is None:
            env_data_target_matrices = Utils.convert_raster_stack_list_into_matrix_list(
                self.parameters_set.env_data_target)
        else:
            env_data_target_matrices = self.rotate_climate_data(reference)
        similarity_data = self.compute_similarity_data(reference, env_data_target_matrices)
        if self.parameters_set.writefile:
            return Utils.create_tiff_file_from_array(similarity_data, RESULTS_DIRECTORY,
                                                     self.parameters_set.file_name + ".tif",
                                                     self.parameters_set.env_data_target[0][0])
        return Utils.create_tiff_file_from_array(similarity_data, TMP_DIRECTORY,
                                                 self.parameters_set.file_name + ".tif",
                                                 self.parameters_set.env_data_target[0][0])

    def rotate_climate_data(self, reference: Site) -> list[np.ndarray]:
        rotation_data = self.compute_rotation_data(reference)
        env_data_target_matrices = []
        for env_var in ("prec", "tmean", "tmin", "tmax"):
            if env_var in self.parameters_set.env_vars:
                index = self.parameters_set.env_vars.index(env_var)
                env_data_target_matrix = Utils.convert_raster_stack_into_matrix(
                    self.parameters_set.env_data_target[index])
                valid_values_indices = np.where(~np.isnan(rotation_data))[0]
                for index in valid_values_indices:
                    env_data_target_matrix[index, :] = self.perform_line_rotation(rotation_data[index],
                                                                                  env_data_target_matrix[index, :])
                env_data_target_matrices.append(env_data_target_matrix)
        return env_data_target_matrices

    def compute_rotation_data(self, reference: Site) -> np.ndarray:
        if self.parameters_set.rotation in ("prec", "tmean"):
            specific_env_data_reference_vector = np.array(reference.env_data[self.parameters_set.rotation])
            specific_env_data_target_paths = self.parameters_set.env_data_target[
                self.parameters_set.env_vars.index(self.parameters_set.rotation)]
            specific_env_data_target_matrix = Utils.convert_raster_stack_into_matrix(specific_env_data_target_paths)
            first_column_specific_env_data_target_matrix = specific_env_data_target_matrix[:, 0]
            rotation_data = np.array([np.nan] * len(first_column_specific_env_data_target_matrix))
            valid_values_indices = np.where(~np.isnan(first_column_specific_env_data_target_matrix))[0]
            for index in valid_values_indices:
                if not np.any(np.isnan(specific_env_data_target_matrix[index])):
                    rotation_data[index] = Utils.compute_rotation_coefficient(specific_env_data_reference_vector,
                                                                              specific_env_data_target_matrix[index])
                else:
                    rotation_data[index] = 0
        else:
            specific_env_data_reference_matrix = np.array([reference.env_data["tmean"], reference.env_data["prec"]])
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
                rotation_data[index] = Utils.compute_rotation_coefficient(specific_env_data_reference_matrix,
                                                                          np.array([first_row, last_row]))
        return rotation_data

    def perform_line_rotation(self, rotation_coefficient: int, matrix_line: np.ndarray) -> np.ndarray:
        if self.parameters_set.rotation in self.parameters_set.env_vars:
            number_divisions = self.parameters_set.number_divisions[
                self.parameters_set.env_vars.index(self.parameters_set.rotation)]
        else:
            number_divisions = self.parameters_set.number_divisions[self.parameters_set.env_vars.index("prec")]
        rotation_coefficient = int(rotation_coefficient)
        if rotation_coefficient == 0 or abs(rotation_coefficient) == number_divisions:
            return matrix_line
        elif rotation_coefficient >= 1:
            return np.concatenate((matrix_line[rotation_coefficient:], matrix_line[:rotation_coefficient]))
        else:
            return np.concatenate((matrix_line[rotation_coefficient:],
                                   matrix_line[: rotation_coefficient + number_divisions]))

    def compute_similarity_data(self, reference: Site, env_data_target_matrices: list[np.ndarray]) -> np.ndarray:
        temp_dissimilarity_data = np.full((env_data_target_matrices[0].shape[0], len(self.parameters_set.env_vars)),
                                          np.nan)
        for i, env_variable in enumerate(self.parameters_set.env_vars):
            if len(reference.env_data[env_variable]) == 1:
                result = np.where(
                    np.isnan(env_data_target_matrices[i]) | np.isnan(reference.env_data[env_variable]),
                    np.nan,
                    (env_data_target_matrices[i] - reference.env_data[env_variable]) ** 2
                )
                result = Utils.perform_distance_normalization(np.sqrt(result), env_variable)
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
            else:
                temp_matrix = np.full((env_data_target_matrices[0].shape[0], self.parameters_set.number_divisions[i]),
                                      np.nan)
                growing_season_indices = np.array(self.parameters_set.growing_season) - 1
                first_matrix = env_data_target_matrices[i][:, growing_season_indices]
                second_matrix = np.array(reference.env_data[env_variable])[growing_season_indices]
                temp_matrix[:, growing_season_indices] = np.square(first_matrix - second_matrix)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    result = Utils.perform_distance_normalization(np.sqrt(np.nanmean(temp_matrix, axis=1)),
                                                                  env_variable)
                temp_dissimilarity_data[:, i] = np.squeeze(result * self.parameters_set.weights[i])
        combined = np.full(env_data_target_matrices[0].shape[0], np.nan)
        if len(self.parameters_set.env_vars) > 1:
            combined[:] = np.round(np.sum(temp_dissimilarity_data, axis=1), decimals=3)
        else:
            combined[:] = np.round(temp_dissimilarity_data[:], decimals=3)
        return combined
