from analogues.parameters_set import ParametersSet, Site
from analogues.utils import Utils
import numpy as np
from osgeo import gdal


class Similarity:
    """
        parameters_set (ParametersSet) : set of parameters used to compute the agro ecology similarity
    """

    def __init__(self, parameters_set: ParametersSet):
        self.parameters_set = parameters_set

    def similarity(self):
        reference = Site(self.parameters_set.longitude, self.parameters_set.latitude, self.parameters_set.env_vars,
                         self.parameters_set.env_data_ref)

    def compute_rotation(self, reference_vector: list[float], target_env_data_row: any) -> float:
        return 0

    def rotate_climate_data(self, reference: Site, parameters_set: ParametersSet):
        file_path = ""
        if parameters_set.rotation in ("prec", "tmean"):
            specific_env_data_reference_vector = reference.env_data[parameters_set.rotation]
            specific_env_data_target_paths = parameters_set.env_data_targ[
                parameters_set.env_vars.index(parameters_set.rotation)]
            specific_env_data_target_matrix = Utils.convert_raster_stack_into_matrix(specific_env_data_target_paths)
            rotation_data = specific_env_data_target_matrix[:, 0]
            valid_values_indices = np.where(~np.isnan(rotation_data))[0]
            for indice in valid_values_indices:
                if not np.any(np.isnan(specific_env_data_target_matrix[indice])):
                    rotation_data[indice] = self.compute_rotation(specific_env_data_reference_vector,
                                                                  specific_env_data_target_matrix[indice])
                else:
                    rotation_data[indice] = 0
            file_path = Utils.create_tiff_file_from_array(rotation_data, "rotation.tif",
                                                          specific_env_data_target_paths[0])
        else:
            specific_env_data_reference_matrix = np.array([reference.env_data["tmean"], reference.env_data["prec"]])
            index_tmean, index_prec = parameters_set.env_vars.index("tmean"), parameters_set.env_vars.index("prec")
            specific_env_data_target_matrix = Utils.convert_raster_stack_list_into_matrix([
                parameters_set.env_data_targ[index_tmean], parameters_set.env_data_targ[index_prec]])
            rotation_data = specific_env_data_target_matrix[:, 0]
            valid_values_indices = np.where(~np.isnan(rotation_data))[0]
            num_div = parameters_set.number_divisions[0]
            num_div2 = 2 * num_div
            for indice in valid_values_indices:
                first_row = specific_env_data_target_matrix[indice, :num_div]
                last_row = specific_env_data_target_matrix[indice, num_div:num_div2]
                rotation_data[indice] = self.compute_rotation(specific_env_data_reference_matrix,
                                                              np.array([first_row, last_row]))
            file_path = Utils.create_tiff_file_from_array(rotation_data, "rotation.tif",
                                                          parameters_set.env_data_targ[0][0])
        return file_path

