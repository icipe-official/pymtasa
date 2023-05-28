from osgeo import gdal
from analogues.static_variables import TMP_DIRECTORY
import numpy as np
import os


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
        x_off, y_off = map(int, offsets)
        return raster.GetRasterBand(1).ReadAsArray(x_off, y_off, 1, 1)[0, 0]

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
        matrix = np.zeros((dimensions[0]*dimensions[1], len(raster_stack)))
        for i, raster_path in enumerate(raster_stack):
            raster = gdal.Open(raster_path)
            band = raster.GetRasterBand(1)
            values = band.ReadAsArray()
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
        for i, raster_stack in enumerate(raster_stack_list):
            for j, raster_path in enumerate(raster_stack):
                raster = gdal.Open(raster_path)
                band = raster.GetRasterBand(1)
                values = band.ReadAsArray()
                values[values == band.GetNoDataValue()] = np.nan
                matrix[:, column_index] = values.ravel()
                raster = None
                column_index += 1
        return matrix

    @staticmethod
    def create_tiff_file_from_array(vector: np.ndarray, tif_name: str, reference_tif_file_path: str) -> str:
        gtiff_driver = gdal.GetDriverByName('GTiff')
        raster = gdal.Open(reference_tif_file_path)
        band = raster.GetRasterBand(1)
        file_path = os.path.join(TMP_DIRECTORY, tif_name)
        out_ds = gtiff_driver.Create(file_path, band.XSize, band.YSize, 1, band.DataType)
        out_ds.SetProjection(raster.GetProjection())
        out_ds.SetGeoTransform(raster.GetGeoTransform())
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(vector.reshape(band.YSize, band.XSize))
        out_ds.FlushCache()
        out_band.ComputeStatistics(True)
        del out_ds
        raster = None
        return file_path



