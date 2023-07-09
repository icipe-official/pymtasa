from afsa.parameters_set import ParametersSet
from afsa.similarity import Similarity
from afsa.utils import Utils
from afsa.static_variables import RESULTS_DIRECTORY, RASTER_STACK_ENV_DATA
import time

if __name__ == '__main__':
    start_time = time.time()
    parameters = ParametersSet(
        longitude=-2.1949567,
        latitude=7.31909,
        env_vars=("prec", "tmean", "rsds", "wdsp"),
        weights=(0.25, 0.35, 0.2, 0.2),
        number_divisions=(12, 12, 12, 12),
        env_data_ref=RASTER_STACK_ENV_DATA,
        env_data_target=RASTER_STACK_ENV_DATA,
        analysis_period=[8, 12],
        rotation="both",
        threshold=0,
        rotation_mode=True,
        threshold_mode=True,
        outfile=RESULTS_DIRECTORY,
        file_name="results",
        write_file=True
    )

    similarity = Similarity(parameters)

    raster_file_path = similarity.compute_similarity_raster(start_time)

    print("Overall Process : ----%.2f----" % (time.time() - start_time))

    # Utils.plot_raster_file(raster_file_path, parameters.longitude, parameters.latitude)
