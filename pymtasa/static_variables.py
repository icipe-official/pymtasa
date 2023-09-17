import os

CSV_DIRECTORY = "/home/tofrano/Documents/WORKSPACE/PYMTASA/Csv"
RESULTS_DIRECTORY = "/home/tofrano/Documents/WORKSPACE/PYMTASA/Results"
NORMALIZATION_COEFFICIENTS = {
    'tmean': 10, 'prec': 50, 'tmin': 10, 'tmax': 10, 'bio_1': 10, 'bio_2': 10, 'bio_3': 10, 'bio_4': 10, 'bio_5': 10,
    'bio_6': 10, 'bio_7': 10, 'bio_8': 10, 'bio_9': 10, 'bio_10': 10, 'bio_11': 10, 'bio_12': 10, 'bio_13': 10,
    'bio_14': 10, 'bio_15': 10, 'bio_16': 10, 'bio_17': 10, 'bio_18': 10, 'bio_19': 10
}
TIME_SERIES_DATASET = [os.path.join(CSV_DIRECTORY, "prec.csv"),
                       os.path.join(CSV_DIRECTORY, "tmean.csv"),
                       ]
QUERY_SEQUENCE = os.path.join(CSV_DIRECTORY, "query_sequence.csv")
HEADERS_INDICES = [[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
