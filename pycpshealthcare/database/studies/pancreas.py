from .results import StudyResults
from .functions import get_pancreas_sensor_results
from ..participant_info import ParticipantInfo

class PancreasStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Pancreas").astype("class")
        

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_fitbit_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results
        

    def get_empatica_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_empatica_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results


    def get_equivital_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_equivital_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results
    

    def get_fitnesspal_ejercicio_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_fitnesspal_ejercicio_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results


    def get_fitnesspal_nutricion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_fitnesspal_nutricion_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results


    def get_guardian_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_guardian_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results
    

    def get_oscar_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.pancreas_group.get_oscar_results(timestamp_start, timestamp_end, specific_test_id, sensors, fields)
        return results
