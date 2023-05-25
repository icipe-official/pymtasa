from analogues.utils import Utils


class ParametersSet:
    def __init__(self, x, y, env_vars, weights, number_divisions, env_data_ref, env_data_targ,
                 growing_season, rotation, threshold, outfile, file_name, writefile):
        """
            x (float) : longitude (decimal degrees) E.g: 5 \n
            y (float) : latitude (decimal degrees) E.g: 5 \n
            env_vars (tuple) : a tuple with the name of the climatic variable(s) to use, e.g. ("prec","tmean"), or
            bioclimatic variable e.g. "bio_1" \n
            weights (tuple) : tuple of length equal to the number of variables. Each value in the vector gives the
            weight given to each variable in the range 0-1. The sum of the weights must equal 1. E.g: (0.5, 0.5) \n
            number_divisions (tuple) : the number of divisions (usually months) for each variable. ndivisions=12 for
            climatic variables and ndivisions=1 for bioclimatic (or other types of variables) variables. E.g: (12,12) \n
            env_data_ref (tuple) : a tuple of length equal to the number of variables that specifies the
            reference climatic conditions. Each element in the list is either a RasterLayer or a RasterStack object.
            RasterLayer applies to bioclimatic variables, whereas RasterStack applies for monthly data. \n
            env_data_targ (tuple) : a tuple of length equal to the number of variables that specifies the target
            climatic conditions. Each element in the list is either a RasterLayer or a RasterStack object. RasterLayer
            applies to bioclimatic variables, whereas RasterStack applies for monthly data. \n
            growing_season (list) : growing season (months) of interest in the analysis. Specified as a vector of
            length 2, where the first value specifies the start and the second value specifies the end of growing
            season. Not relevant for bioclimatic variables. E.g: [1,12] \n
            rotation (string) : should a rotation be applied. i.e. "tmean", "prec", "both" or "none".
            Rotation will allow comparisons between sites with different seasonality (e.g. northern vs. southern
            hemisphere) \n
            threshold (float) : value between 0-1. Only sites with a climatic similarity above this
            threshold will be saved and displayed. \n
            outfile (string) : directory where the resultant similarity map will be saved \n
            file_name (string) :  name of output file \n
            writefile (boolean) : if the output file is to be written on disk. Otherwise, only an object will be
            returned. \n
        """

        self.latitude = y
        self.longitude = x
        self.env_vars = env_vars
        self.weights = weights
        self.number_divisions = number_divisions
        self.env_data_ref = env_data_ref
        self.env_data_targ = env_data_targ
        self.rotation = rotation
        self.threshold = threshold
        self.outfile = outfile
        self.file_name = file_name
        self.writefile = writefile

        if len(growing_season) == 1:
            self.growing_season = growing_season
        elif len(growing_season) == 2 and growing_season[0] > growing_season[1]:
            # E.g : [11, 2] must become [11, 12, 1, 2]
            self.growing_season = list(range(growing_season[0], 13)) + list(range(1, growing_season[1] + 1))
        elif len(growing_season) == 2 and growing_season[0] < growing_season[1]:
            # E.g : [3, 5] must become [3, 4, 5]
            self.growing_season = list(range(growing_season[0], growing_season[1] + 1))
        elif len(growing_season) == 4 and growing_season[0] > growing_season[1]:
            # E.g : [11, 3, 6, 8] must become [11, 12] + [1, 2, 3] + [6, 7, 8] = [11, 12, 1, 2, 3, 6, 7, 8]
            self.growing_season = list(range(growing_season[0], 13)) + list(range(1, growing_season[1] + 1)) + \
                                  list(range(growing_season[2], growing_season[3] + 1))
        elif len(growing_season) == 4 and growing_season[2] > growing_season[3]:
            # E.g : [6, 8, 11, 2] must become [6, 7, 8] + [11, 12] + [1, 2] = [6, 7, 8, 11, 12, 1, 2]
            self.growing_season = list(range(growing_season[0], growing_season[1] + 1)) + \
                                  list(range(growing_season[2], 13)) + list(range(1, growing_season[3] + 1))
        else:
            # E.g : [1, 3, 6, 8] must become [1, 2, 3] + [6, 7, 8] = [1, 2, 3, 6, 7, 8]
            self.growing_season = list(range(growing_season[0], growing_season[1] + 1)) + \
                                  list(range(growing_season[2], growing_season[3] + 1))

        self.growing_season = Utils.remove_duplicates(self.growing_season)


class Site:
    def __init__(self, x, y, env_vars, env_data_ref):
        """
            longitude (float) : longitude (decimal degrees) E.g: 5 \n
            latitude (float) : latitude (decimal degrees) E.g: 5 \n
            env_data (dictionary) : environmental variables corresponding to (y,x).
                E.g : { 'temp': [20, 22, 23], 'prec': [120. 152, 133] }
        """

        self.longitude = x
        self.latitude = y
        self.env_data = {}

        for i, env_data_file_path_set in enumerate(env_data_ref):
            tmp_value_list = [Utils.extract_value_from_tif_with_map_coord(tif_file_path, x, y) for tif_file_path in
                              env_data_file_path_set]
            self.env_data[env_vars[i]] = tmp_value_list



