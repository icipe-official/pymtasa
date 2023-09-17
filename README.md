# PYMTASA (PYthon Multivariate Time series Alignment and Similarity Assessment)

## Overview

PYMTASA is a Python package designed for Multivariate Time series Alignment and Similarity Assessment. This package provides a framework for computing similarity index matrices for multivariate time series data. It's particularly useful for scenarios where temporal shifts need to be considered in the similarity assessment.

## Installation

You can install the dependencies using pip:

```plaintext
pip install -r requirements.txt
```

## Input data

- `measurement_vars` (tuple): Names of the measurements variables to use, e.g. ("prec","tmean").
- `weights` (tuple): Weights for each variable in the range 0-1. The sum of the weights must equal 1, e.g., (0.5, 0.5).
- `number_divisions` (tuple): Number of divisions for each variable, e.g., (12, 12).
- `ref_data` (string): File path of the query sequence data.
- `target_dataset` (tuple): File paths for the time series dataset.
- `headers_indices` (list): List of headers indices corresponding to the measurements values within the time series files.
- `analysis_period` (list): Period of interest in the analysis.
- `rotation_variables` (list): List of rotation variables used for comparing instances with temporal shifts.
- `rotation_mode` (bool): Specify if the rotation is absolute or relative.
- `threshold` (float): Similarity threshold value between 0 and 1.
- `threshold_mode` (bool): Specify if the threshold is absolute or relative.
- `outfile` (string): Directory where the resultant similarity matrix will be saved.
- `file_name` (string): Name of the output file.
- `write_file` (boolean): Whether to write the output file to disk.

## USAGE

Here's an example of how to use PYMTASA:

```python
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
        file_name="pyresults",
        write_file=True
    )

    similarity = Similarity(mtasa_parameters)

    similarity_index_matrix = similarity.compute_similarity_matrix()
```

## Results
The package will compute a similarity index matrix based on the provided parameters. The results can be saved to the specified directory.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
