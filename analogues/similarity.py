from analogues.parameters_set import ParametersSet, Site


class Similarity:
    """
        parameters_set (ParametersSet) : set of parameters used to compute the agro ecology similarity
    """
    def __init__(self, parameters_set: ParametersSet):
        self.parameters_set = parameters_set

    def similarity(self):
        reference = Site(self.parameters_set.longitude, self.parameters_set.latitude, self.parameters_set.env_vars,
                         self.parameters_set.env_data_ref)
