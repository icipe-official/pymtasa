import os

from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np


class Utils:
    @staticmethod
    def remove_duplicates(lst: list) -> list:
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

    @staticmethod
    def extract_value_from_tif_with_map_coord(tif_file_path: str, x: float, y: float) -> float:
        raster = gdal.Open(tif_file_path)
        inv_geo = gdal.InvGeoTransform(raster.GetGeoTransform())
        offsets = gdal.ApplyGeoTransform(inv_geo, x, y)
        x_off, y_off = int(offsets[0]), int(offsets[1])
        matrix = raster.GetRasterBand(1).ReadAsArray(x_off, y_off, 1, 1)[0, 0]
        raster = None
        return matrix

    @staticmethod
    def get_dimension_raster_layer(tif_file_path: str) -> (int, int):
        raster = gdal.Open(tif_file_path)
        band = raster.GetRasterBand(1)
        width = band.XSize
        height = band.YSize
        raster = None
        return width, height

    @staticmethod
    def convert_raster_stack_into_matrix(raster_stack: list[str]) -> np.ndarray:
        dimensions = Utils.get_dimension_raster_layer(raster_stack[0])
        matrix = np.zeros((dimensions[0] * dimensions[1], len(raster_stack)))
        for i, raster_path in enumerate(raster_stack):
            raster = gdal.Open(raster_path)
            band = raster.GetRasterBand(1)
            values = band.ReadAsArray().astype(float)
            values[values == band.GetNoDataValue()] = np.nan
            matrix[:, i] = values.ravel()
            raster = None
        return matrix

    @staticmethod
    def convert_raster_stack_list_into_matrix(raster_stack_list: list[list[str]]) -> np.ndarray:
        num_columns = sum(len(raster_stack) for raster_stack in raster_stack_list)
        dimensions = Utils.get_dimension_raster_layer(raster_stack_list[0][0])
        matrix = np.zeros((dimensions[0] * dimensions[1], num_columns))
        column_index = 0
        for raster_stack in raster_stack_list:
            for raster_path in raster_stack:
                raster = gdal.Open(raster_path)
                band = raster.GetRasterBand(1)
                values = band.ReadAsArray().astype(float)
                values[values == band.GetNoDataValue()] = np.nan
                matrix[:, column_index] = values.ravel()
                raster = None
                column_index += 1
        return matrix

    @staticmethod
    def convert_raster_stack_list_into_matrix_list(raster_stack_list: list[list[str]]) -> list[np.ndarray]:
        matrix_list = []
        for raster_stack in raster_stack_list:
            matrix_list.append(Utils.convert_raster_stack_list_into_matrix([raster_stack]))
        return matrix_list

    @staticmethod
    def compute_rotation_coefficient(rotation_mode: bool, analysis_period: list[int], reference_vector: np.ndarray,
                                     target_env_data_row: np.ndarray) -> float:
        if len(target_env_data_row) == 1:
            return 0

        n = reference_vector.shape[1] if reference_vector.ndim != 1 else len(reference_vector)

        if rotation_mode:
            indices = np.array(analysis_period) - 1
            if reference_vector.ndim == 1:
                analysis_reference_vector = np.zeros(n)
                analysis_reference_vector[indices] = reference_vector[indices]
                fourier1 = np.fft.fft(analysis_reference_vector)
                fourier2 = np.fft.fft(target_env_data_row)
            else:
                analysis_reference_matrix = np.zeros((2, n))
                analysis_reference_matrix[0, indices] = reference_vector[0, :][indices]
                analysis_reference_matrix[1, indices] = reference_vector[1, :][indices]
                fourier1 = np.sum(np.fft.fft(analysis_reference_matrix), axis=0)
                fourier2 = np.sum(np.fft.fft(target_env_data_row), axis=0)
            return (n - np.real(np.fft.ifft(np.conjugate(fourier2) * fourier1)).argmax()) % n
        else:
            if reference_vector.ndim == 1:
                fourier1 = np.fft.fft(reference_vector)
                fourier2 = np.fft.fft(target_env_data_row)
            else:
                fourier1 = np.sum(np.fft.fft(reference_vector), axis=0)
                fourier2 = np.sum(np.fft.fft(target_env_data_row), axis=0)

            highest_frequency_component_pos_fourier1 = np.argmax(np.abs(fourier1[1:]))

            if highest_frequency_component_pos_fourier1 == np.argmax(np.abs(fourier2[1:])):
                phase1 = np.angle(fourier1)
                phase2 = np.angle(fourier2)
                return round(((phase1[highest_frequency_component_pos_fourier1 + 1] - phase2[
                    highest_frequency_component_pos_fourier1 + 1]) * (n / 2)) / np.pi, 0) % n
            else:
                return (n - np.real(np.fft.ifft(np.multiply(fourier1, np.conjugate(fourier2)))).argmax()) % n

    @staticmethod
    def perform_distance_normalization(distances: np.ndarray, normalization_coefficient: int) -> np.array:
        return normalization_coefficient / (normalization_coefficient + distances)

    @staticmethod
    def create_tiff_file_from_array(vector: np.ndarray, directory: str, tif_name: str,
                                    reference_tif_file_path: str) -> str:
        gtiff_driver = gdal.GetDriverByName('GTiff')
        raster = gdal.Open(reference_tif_file_path)
        band = raster.GetRasterBand(1)
        file_path = os.path.join(directory, tif_name)
        out_ds = gtiff_driver.Create(file_path, band.XSize, band.YSize, 1, 6,
                                     options=['TILED=YES', 'COMPRESS=DEFLATE'])
        out_ds.SetProjection(raster.GetProjection())
        out_ds.SetGeoTransform(raster.GetGeoTransform())
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(vector.reshape(band.YSize, band.XSize))
        out_ds.FlushCache()
        out_band.ComputeStatistics(True)
        del out_ds
        raster = None
        return file_path

    @staticmethod
    def plot_raster_file(file_path: str, longitude: float, latitude: float):
        ds = gdal.Open(file_path)
        data = ds.GetRasterBand(1).ReadAsArray()
        cmap = plt.cm.get_cmap('RdYlGn')
        plt.imshow(data, cmap=cmap)
        plt.colorbar()
        x, y = map(int, gdal.ApplyGeoTransform(gdal.InvGeoTransform(ds.GetGeoTransform()), longitude, latitude))
        plt.scatter(x, y, s=50, c='#00faf6', marker='X')
        plt.show()
        ds = None
