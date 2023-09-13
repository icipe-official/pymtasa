import csv
from pymtasa.utils import Utils


class ParametersSet:
    def __init__(self, longitude: float, latitude: float, env_vars: tuple, weights: tuple, number_divisions: tuple,
                 env_data_ref: list[list[str]], env_data_target: list[list[str]], analysis_period: list[int],
                 rotation: str, rotation_mode: bool, threshold: float, threshold_mode: bool, outfile: str,
                 file_name: str, write_file: bool):
        """
            longitude (float) : longitude (decimal degrees) E.g: 5 \n
            latitude (float) : latitude (decimal degrees) E.g: 5 \n
            env_vars (tuple) : a tuple with the name of the climatic variable(s) to use, e.g. ("prec","tmean"), or
                bioclimatic variable e.g. "bio_1" \n
            weights (tuple) : tuple of length equal to the number of variables. Each value in the vector gives the
                weight given to each variable in the range 0-1. The sum of the weights must equal 1. E.g: (0.5, 0.5) \n
            number_divisions (tuple) : the number of divisions (usually months) for each variable. ndivisions=12 for
                climatic variables and ndivisions=1 for bioclimatic (or other types of variables) variables.
                E.g: (12,12) \n
            env_data_ref (tuple) : a tuple of length equal to the number of variables that specifies the
                reference climatic conditions. Each element in the list is either a RasterLayer or a RasterStack object.
                RasterLayer applies to bioclimatic variables, whereas RasterStack applies for monthly data. \n
            env_data_target (tuple) : a tuple of length equal to the number of variables that specifies the target
                climatic conditions. Each element in the list is either a RasterLayer or a RasterStack object.
                RasterLayer applies to bioclimatic variables, whereas RasterStack applies for monthly data. \n
            analysis_period (list) : period (months) of interest in the analysis. c Not relevant for bioclimatic
                variables. E.g: [1,12] \n
            rotation (string) : should a rotation be applied. i.e. "tmean", "prec", "both" or "none".
                Rotation will allow comparisons between sites with different seasonality (e.g. northern vs. southern
                hemisphere) \n
            rotation_mode (bool) : specify if the rotation will be absolute (i.e. the analysis period is used as basis)
                or relative (i.e. the whole year will be used as abasis). True for absolute mode, False for relative
                mode \n
            threshold (float) : value between 0-1. Only sites with a climatic similarity above this threshold will be
                saved and displayed. \n
            threshold_mode (bool) : specify if the threshold is an absolute or relative value. True for absolute value,
                False for relative values \n
            outfile (string) : directory where the resultant similarity map will be saved \n
            file_name (string) :  name of output file \n
            write_file (boolean) : if the output file is to be written on disk. Otherwise, only an object will be
                returned. \n

            Note :  The position of the variables in env_vars must follow the same order as the position of the
                    variables in number_divisions, env_data_ref & env_data_target
        """

        self.longitude = longitude
        self.latitude = latitude
        self.env_vars = env_vars
        self.weights = weights
        self.number_divisions = number_divisions
        self.env_data_ref = env_data_ref
        self.env_data_target = env_data_target
        self.analysis_period = analysis_period
        self.rotation = rotation
        self.threshold = threshold
        self.rotation_mode = rotation_mode
        self.threshold_mode = threshold_mode
        self.outfile = outfile
        self.file_name = file_name
        self.write_file = write_file


class Site:
    def __init__(self, x: float, y: float, env_vars: tuple, env_data_ref: list[list[str]]):
        """
            longitude (float) : longitude (decimal degrees) E.g: 5 \n
            latitude (float) : latitude (decimal degrees) E.g: 5 \n
            env_data (dictionary) : environmental variables corresponding to (x,y).
                E.g : { 'temp': [20, 22, 23], 'prec': [120, 152, 133] }
        """

        self.longitude = x
        self.latitude = y
        self.env_data = {}

        for i, env_data_file_path_set in enumerate(env_data_ref):
            tmp_value_list = [Utils.extract_value_from_tif_with_map_coord(tif_file_path, x, y) for tif_file_path in
                              env_data_file_path_set]
            self.env_data[env_vars[i]] = tmp_value_list


class MTASAParametersSet:
    def __init__(self, measurement_vars: tuple, weights: tuple, number_divisions: tuple, ref_data: str,
                 target_data: list[str], headers_indices: list[list[int]], analysis_period: list[int],
                 rotation: list[str], rotation_mode: bool, threshold: float, threshold_mode: bool, outfile: str,
                 file_name: str, write_file: bool):
        """
            measurement_vars (tuple) : a tuple with the name of the measurements variable(s) to use,
                e.g. ("prec","tmean") \n
            weights (tuple) : tuple of length equal to the number of variables. Each value in the vector gives the
                weight given to each variable in the range 0-1. The sum of the weights must equal 1. E.g: (0.5, 0.5) \n
            number_divisions (tuple) : the number of divisions for each variable. E.g: (12,12) \n
            ref_data (string) : File path of the file containing the data for the query sequence \n
            target_data (tuple) : a tuple of length equal to the number of variables that specifies the time
                series dataset \n
            headers_indices (list): list of headers indices corresponding to the measurements values within the files
                representing the time series dataset. E.g: [2, 3, 4] \n
            analysis_period (list) : period of interest in the analysis. E.g: [1,12] \n
            rotation (list) : should a rotation be applied. i.e. "tmean", "prec", "both" or "none".
                Rotation will allow comparisons between instances with temporal shift \n
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
        self.target_data = target_data
        self.headers_indices = headers_indices
        self.analysis_period = analysis_period
        self.rotation = rotation
        self.threshold = threshold
        self.rotation_mode = rotation_mode
        self.threshold_mode = threshold_mode
        self.outfile = outfile
        self.file_name = file_name
        self.write_file = write_file


class MTASASite:
    def __init__(self, measurement_vars: tuple, query_sequence_file_path: str):
        """
            data (dictionary) : measurements variables corresponding to (x,y).
                E.g : { 'temp': [20, 22, 23], 'prec': [120, 152, 133] }
        """

        self.data = {}

        with open(query_sequence_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            matrix = [[value for key, value in row.items() if key != ''] for row in reader]
            self.data = {measurement_vars[i]: [matrix[i][j] for j in [*range(1, len(matrix[0]))]] for i in
                         range(len(measurement_vars))}
