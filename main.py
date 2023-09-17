from pymtasa.parameters_set import ParametersSet
from pymtasa.similarity import Similarity
from pymtasa.static_variables import RESULTS_DIRECTORY, TIME_SERIES_DATASET, QUERY_SEQUENCE, HEADERS_INDICES

if __name__ == '__main__':
    mtasa_parameters = ParametersSet(
        measurement_vars=("prec", "tmean"),
        weights=(0.5, 0.5),
        number_divisions=(12, 12),
        ref_data=QUERY_SEQUENCE,
        target_dataset=TIME_SERIES_DATASET,
        headers_indices=HEADERS_INDICES,
        analysis_period=[11, 12],
        rotation_variables=["prec", "tmean"],
        threshold=0,
        rotation_mode=True,
        threshold_mode=True,
        outfile=RESULTS_DIRECTORY,
        file_name="similarity",
        write_file=True
    )

    similarity = Similarity(mtasa_parameters)

    similarity_index_matrix = similarity.compute_similarity_matrix()