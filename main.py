from parameters_set import ParametersSet, Site


def test():

    parameters_set = ParametersSet(
        5.34,
        5.33,
        ("prec", "tmean"),
        (0.5, 0.5),
        12,
        [
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_feb.tif"],
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_feb.tif"]
        ],
        [
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_feb.tif"],
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_feb.tif"]
        ],
        [1, 12],
        "tmean",
        1,
        "~/Documents/WORKSPACE/PYTHON-CCAFS/results",
        "results.tif",
        True
    )

    site = Site(
        -75.5,
        3.2,
        ("prec", "tmean"),
        [
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/prec_feb.tif"],
            ["/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_jan.tif",
             "/home/tofrano/Documents/WORKSPACE/Franck/Tifs/tavg_feb.tif"]
        ]
    )

    print(site.env_data)


if __name__ == '__main__':
    # Perform tests to check the different class and functions
    test()
