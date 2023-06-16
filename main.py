from analogues.parameters_set import ParametersSet, Site
from analogues.similarity import Similarity
from analogues.utils import Utils
from analogues.static_variables import TIFS_DIRECTORY, RESULTS_DIRECTORY
import os
import numpy as np


def test():
    parameters = ParametersSet(
        5.34,
        5.33,
        ("prec", "tmean"),
        (0.5, 0.5),
        (2, 2),
        [
            [os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif")],
            [os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif")]
        ],
        [
            [os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif")],
            [os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif")]
        ],
        [1, 12],
        "both",
        1,
        RESULTS_DIRECTORY,
        "results.tif",
        True
    )

    site = Site(
        9.94,
        5.55,
        ("prec", "tmean"),
        [
            [os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif")],
            [os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif")]
        ]
    )

    similarity = Similarity(parameters)

    similarity.compute_similarity_raster()

    # Utils.convert_raster_stack_list_into_matrix_list(parameters.env_data_target)

    # similarity.compute_rotation_data(site, parameters)

    # arr1 = np.array( [[20, 20, 20, 20, 20, 19, 19, 20, 20, 20, 20, 20], [85, 104, 139, 202, 198, 173, 138, 121,
    # 134, 220, 192, 121]])
    # arr2 = np.array([[-3.163398, -4.024446, 1.828977, 11.24864, 18.34279, 22.86018,
    # 25.572027, 25.444578, 19.25178, 12.03754, 5.183794, -1.404339], [7.097222, 7.243055, 11.923611, 15.72222,
    # 14.02083, 10.07639, 9.548611, 8.458333, 9.68750, 10.97917, 12.805555, 10.437500]])
    #
    # similarity.compute_rotation(arr1, arr2)

    # similarity.compute_rotation([20, 20, 20, 20, 20, 19, 19, 20, 20, 20, 20, 20], [-37.89279, -38.65754, -37.76574,
    # -28.28976, -13.78938, -2.490278, 2.866148, -0.1539603, -8.533901, -21.92391, -31.0105, -35.319])

    # Utils.convert_raster_stack_list_into_matrix([
    #         [os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif")],
    #         [os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif")]
    #     ])

    # print(dimensions[0]*dimensions[1])


if __name__ == '__main__':
    # Perform tests to check the different class and functions
    test()
