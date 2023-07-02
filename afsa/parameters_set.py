from afsa.utils import Utils


class ParametersSet:
    def __init__(self, longitude: float, latitude: float, env_vars: tuple, weights: tuple, number_divisions: tuple,
                 env_data_ref: list[list[str]], env_data_target: list[list[str]], growing_season: list[int],
                 rotation: str, threshold: float, absolute_mode: bool, outfile: str, file_name: str, write_file: bool):
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
            growing_season (list) : growing season (months) of interest in the analysis. c Not relevant for bioclimatic
                variables. E.g: [1,12] \n
            rotation (string) : should a rotation be applied. i.e. "tmean", "prec", "both" or "none".
                Rotation will allow comparisons between sites with different seasonality (e.g. northern vs. southern
                hemisphere) \n
            threshold (float) : value between 0-1. Only sites with a climatic similarity above this threshold will be
                saved and displayed. \n
            absolute_mode (bool) : specify if the threshold is an absolute or relative value. True for absolute value,
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
        self.growing_season = growing_season
        self.rotation = rotation
        self.threshold = threshold
        self.absolute_mode = absolute_mode
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
