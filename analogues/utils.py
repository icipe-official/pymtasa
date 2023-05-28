from osgeo import gdal


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
