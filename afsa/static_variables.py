import os

TMP_DIRECTORY = "/home/tofrano/Downloads"
TIFS_DIRECTORY = "/home/tofrano/Documents/WORKSPACE/Franck/Tifs2"
RESULTS_DIRECTORY = "/home/tofrano/Documents/WORKSPACE/PYTHON-CCAFS/results"
NORMALIZATION_COEFFICIENTS = {
    'tmean': 10, 'prec': 50, 'tmin': 10, 'tmax': 10, 'bio_1': 10, 'bio_2': 10, 'bio_3': 10, 'bio_4': 10, 'bio_5': 10,
    'bio_6': 10, 'bio_7': 10, 'bio_8': 10, 'bio_9': 10, 'bio_10': 10, 'bio_11': 10, 'bio_12': 10, 'bio_13': 10,
    'bio_14': 10, 'bio_15': 10, 'bio_16': 10, 'bio_17': 10, 'bio_18': 10, 'bio_19': 10
}
RASTER_STACK_ENV_DATA = [
        [
            os.path.join(TIFS_DIRECTORY, "prec_jan.tif"), os.path.join(TIFS_DIRECTORY, "prec_feb.tif"),
            os.path.join(TIFS_DIRECTORY, "prec_mar.tif"), os.path.join(TIFS_DIRECTORY, "prec_apr.tif"),
            os.path.join(TIFS_DIRECTORY, "prec_may.tif"), os.path.join(TIFS_DIRECTORY, "prec_jun.tif"),
            os.path.join(TIFS_DIRECTORY, "prec_jul.tif"), os.path.join(TIFS_DIRECTORY, "prec_aug.tif"),
            os.path.join(TIFS_DIRECTORY, "prec_sep.tif"), os.path.join(TIFS_DIRECTORY, "prec_oct.tif"),
            os.path.join(TIFS_DIRECTORY, "prec_nov.tif"), os.path.join(TIFS_DIRECTORY, "prec_dec.tif")
        ],
        [
            os.path.join(TIFS_DIRECTORY, "tavg_jan.tif"), os.path.join(TIFS_DIRECTORY, "tavg_feb.tif"),
            os.path.join(TIFS_DIRECTORY, "tavg_mar.tif"), os.path.join(TIFS_DIRECTORY, "tavg_apr.tif"),
            os.path.join(TIFS_DIRECTORY, "tavg_may.tif"), os.path.join(TIFS_DIRECTORY, "tavg_jun.tif"),
            os.path.join(TIFS_DIRECTORY, "tavg_jul.tif"), os.path.join(TIFS_DIRECTORY, "tavg_aug.tif"),
            os.path.join(TIFS_DIRECTORY, "tavg_sep.tif"), os.path.join(TIFS_DIRECTORY, "tavg_oct.tif"),
            os.path.join(TIFS_DIRECTORY, "tavg_nov.tif"), os.path.join(TIFS_DIRECTORY, "tavg_dec.tif")
        ]
    ]
