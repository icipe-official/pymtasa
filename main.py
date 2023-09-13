from pymtasa.parameters_set import ParametersSet, MTASAParametersSet
from pymtasa.similarity import Similarity, MTASASimilarity
from pymtasa.utils import Utils
from pymtasa.static_variables import RESULTS_DIRECTORY, RASTER_STACK_ENV_DATA
import time

if __name__ == '__main__':
    start_time = time.time()
    parameters = ParametersSet(
        longitude=35.12518,
        latitude=-15.06001,
        env_vars=("prec", "tmean"),
        weights=(0.5, 0.5),
        number_divisions=(12, 12),
        env_data_ref=RASTER_STACK_ENV_DATA,
        env_data_target=RASTER_STACK_ENV_DATA,
        analysis_period=[11, 12],
        rotation="both",
        threshold=0,
        rotation_mode=True,
        threshold_mode=True,
        outfile=RESULTS_DIRECTORY,
        file_name="pyresults",
        write_file=True
    )

    mtasa_parameters = MTASAParametersSet(
        measurement_vars=("prec", "tmean"),
        weights=(0.5, 0.5),
        number_divisions=(12, 12),
        ref_data="/Users/francktonle/Downloads/OTHERS/Csv/query_sequence.csv",
        target_data=["/Users/francktonle/Downloads/OTHERS/Csv/prec.csv",
                     "/Users/francktonle/Downloads/OTHERS/Csv/tmean.csv"],
        headers_indices=[[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
        analysis_period=[11, 12],
        rotation=["prec"],
        threshold=0,
        rotation_mode=True,
        threshold_mode=True,
        outfile=RESULTS_DIRECTORY,
        file_name="pyresults",
        write_file=True
    )

    similarity = Similarity(parameters)

    raster_file_path = similarity.compute_similarity_raster(start_time)

    # mtasa_similarity = MTASASimilarity(mtasa_parameters)
    #
    # similarity_matrix_file_path = mtasa_similarity.compute_similarity_matrix(start_time)

    print("Overall Process : ----%.2f----" % (time.time() - start_time))

    Utils.plot_raster_file(raster_file_path, parameters.longitude, parameters.latitude)
