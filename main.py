from pymtasa.parameters_set import ParametersSet
from pymtasa.similarity import Similarity
from pymtasa.static_variables import RESULTS_DIRECTORY
import time

if __name__ == '__main__':
    start_time = time.time()

    mtasa_parameters = ParametersSet(
        measurement_vars=("prec", "tmean"),
        weights=(0.5, 0.5),
        number_divisions=(12, 12),
        ref_data="/home/tofrano/Documents/WORKSPACE/PYMTASA/Csv/query_sequence.csv",
        target_dataset=["/home/tofrano/Documents/WORKSPACE/PYMTASA/Csv/prec.csv",
                        "/home/tofrano/Documents/WORKSPACE/PYMTASA/Csv/tmean.csv"],
        headers_indices=[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
        analysis_period=[11, 12],
        rotation_variables=["prec", "tmean"],
        threshold=0,
        rotation_mode=True,
        threshold_mode=True,
        outfile=RESULTS_DIRECTORY,
        file_name="pyresults",
        write_file=True
    )

    similarity = Similarity(mtasa_parameters)

    similarity_index_matrix = similarity.compute_similarity_matrix(start_time)

    print("Overall Process : ----%.2f----" % (time.time() - start_time))
