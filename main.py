from analogues.parameters_set import ParametersSet, Site
from analogues.similarity import Similarity
from analogues.utils import Utils
from analogues.static_variables import TIFS_DIRECTORY, RESULTS_DIRECTORY
import os


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
    similarity.rotate_climate_data(site, parameters)

    # Utils.convert_raster_stack_list_into_matrix([
    #         [os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif")],
    #         [os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif")]
    #     ])

    # print(dimensions[0]*dimensions[1])


if __name__ == '__main__':
    # Perform tests to check the different class and functions
    test()
