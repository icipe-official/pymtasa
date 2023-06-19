import os
from analogues.parameters_set import ParametersSet
from analogues.similarity import Similarity
from analogues.utils import Utils
from analogues.static_variables import TIFS_DIRECTORY, RESULTS_DIRECTORY


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
        [1, 2],
        "both",
        1,
        RESULTS_DIRECTORY,
        "results",
        False
    )

    similarity = Similarity(parameters)

    raster_file_path = similarity.compute_similarity_raster()

    Utils.plot_raster_file(raster_file_path)


if __name__ == '__main__':
    # Perform tests to check the different class and functions
    test()
