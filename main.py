from analogues.parameters_set import ParametersSet, Site


def test():

    parameters = ParametersSet(
        5.34,
        5.33,
        ("prec", "tmean"),
        (0.5, 0.5),
        12,
        [
            ["/Users/francktonle/Downloads/OTHERS/Tifs/prec_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/prec_feb.tif"],
            ["/Users/francktonle/Downloads/OTHERS/Tifs/tavg_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/tavg_feb.tif"]
        ],
        [
            ["/Users/francktonle/Downloads/OTHERS/Tifs/prec_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/prec_feb.tif"],
            ["/Users/francktonle/Downloads/OTHERS/Tifs/tavg_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/tavg_feb.tif"]
        ],
        [1, 12],
        "tmean",
        1,
        "~/Documents/WORKSPACE/PYTHON-CCAFS/results",
        "results.tif",
        True
    )

    site = Site(
        9.94,
        5.45,
        ("prec", "tmean"),
        [
            ["/Users/francktonle/Downloads/OTHERS/Tifs/prec_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/prec_feb.tif"],
            ["/Users/francktonle/Downloads/OTHERS/Tifs/tavg_jan.tif",
             "/Users/francktonle/Downloads/OTHERS/Tifs/tavg_feb.tif"]
        ]
    )

    print(site.env_data)


if __name__ == '__main__':
    # Perform tests to check the different class and functions
    test()
