import csv


class ParametersSet:
    def __init__(self, measurement_vars: tuple, weights: tuple, number_divisions: tuple, ref_data: str,
                 target_dataset: list[str], headers_indices: list[list[int]], analysis_period: list[int],
                 rotation_variables: list[str], rotation_mode: bool, threshold: float, threshold_mode: bool,
                 outfile: str, file_name: str, write_file: bool):
        """
            measurement_vars (tuple) : a tuple with the name of the measurements variable(s) to use,
                e.g. ("prec","tmean") \n
            weights (tuple) : tuple of length equal to the number of variables. Each value in the vector gives the
                weight given to each variable in the range 0-1. The sum of the weights must equal 1. E.g: (0.5, 0.5) \n
            number_divisions (tuple) : the number of divisions for each variable. E.g: (12,12) \n
            ref_data (string) : File path of the file containing the data for the query sequence \n
            target_dataset (tuple) : a tuple of length equal to the number of variables that specifies the time
                series dataset \n
            headers_indices (list): list of headers indices corresponding to the measurements values within the files
                representing the time series dataset. E.g: [2, 3, 4] \n
            analysis_period (list) : period of interest in the analysis. E.g: [1,12] \n
            rotation_variables (list) : list of rotation variables that will be used to compare instances with temporal
                shift. E.g: ["prec"] \n
            rotation_mode (bool) : specify if the rotation will be absolute (i.e. the analysis period is used as basis)
                or relative (i.e. the whole measurement period will be used as a basis). True for absolute mode, False
                for relative mode \n
            threshold (float) : value between 0-1. Only instances with a  similarity above this threshold will be saved
                and displayed. \n
            threshold_mode (bool) : specify if the threshold is an absolute or relative value. True for absolute value,
                False for relative values \n
            outfile (string) : directory where the resultant similarity matrix will be saved \n
            file_name (string) :  name of output file \n
            write_file (boolean) : if the output file is to be written on disk. Otherwise, only an object will be
                returned. \n

            Note :  The position of the variables in vars must follow the same order as the position of the variables in
                number_divisions, env_data_ref & env_data_target
        """

        self.measurement_vars = measurement_vars
        self.weights = weights
        self.number_divisions = number_divisions
        self.ref_data = ref_data
        self.target_dataset = target_dataset
        self.headers_indices = headers_indices
        self.analysis_period = analysis_period
        self.rotation_variables = rotation_variables
        self.threshold = threshold
        self.rotation_mode = rotation_mode
        self.threshold_mode = threshold_mode
        self.outfile = outfile
        self.file_name = file_name
        self.write_file = write_file


class QuerySequence:
    def __init__(self, measurement_vars: tuple, query_sequence_file_path: str):
        """
            data (dictionary) : measurements variables corresponding to (x,y).
                E.g : { 'temp': [20, 22, 23], 'prec': [120, 152, 133] }
        """

        self.data = {}

        with open(query_sequence_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            matrix = [[float(value) for key, value in row.items() if key != ''] for row in reader]
            self.data = {measurement_vars[i]: [matrix[i][j] for j in [*range(0, len(matrix[0]))]] for i in
                         range(len(measurement_vars))}