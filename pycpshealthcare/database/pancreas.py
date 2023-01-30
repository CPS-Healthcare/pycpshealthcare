from .results import StudyResults
from .participant_info import ParticipantInfo
from .pancreas_functions import get_pancreas_sensor_results

class PancreasStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Pancreas").astype("participant")
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["Pancreas"]]


    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["fitbit"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_empatica_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["empatica"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_equivital_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["equivital"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_fitnesspal_ejercicio_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["fitnesspal_ejercicio"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

    def get_fitnesspal_nutricion_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["fitnesspal_nutricion"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

    def get_guardian_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["guardian"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_oscar_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["oscar"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
