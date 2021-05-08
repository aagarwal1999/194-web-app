

class Metrics:
    def __init__(self, path_to_medical_dict):
        f = open(path_to_medical_dict, "r")
        self.medical_dict = set(f.read().split("\n"))

    def compute_metrics(self, dataset):
        for item in dataset:
            pass



