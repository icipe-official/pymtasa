from afsa.parameters_set import ParametersSet
from afsa.similarity import Similarity
from afsa.utils import Utils
from afsa.static_variables import RESULTS_DIRECTORY, RASTER_STACK_ENV_DATA

if __name__ == '__main__':
    parameters = ParametersSet(
        longitude=5.34,
        latitude=5.33,
        env_vars=("prec", "tmean"),
        weights=(0.5, 0.5),
        number_divisions=(12, 12),
        env_data_ref=RASTER_STACK_ENV_DATA,
        env_data_target=RASTER_STACK_ENV_DATA,
        growing_season=[1, 3],
        rotation="both",
        threshold=0.2,
        absolute_mode=False,
        outfile=RESULTS_DIRECTORY,
        file_name="results",
        write_file=False
    )

    similarity = Similarity(parameters)

    raster_file_path = similarity.compute_similarity_raster()

    Utils.plot_raster_file(raster_file_path, parameters.longitude, parameters.latitude)
