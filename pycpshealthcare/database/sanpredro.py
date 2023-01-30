from .results import StudyResults
from .participant_info import ParticipantInfo
from .sanpredro_functions import get_sanpredro_sensor_results

class SanPedroStudy:

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
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_alimentacion_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["alimentacion"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_patrones_minsal_2018_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["patrones_minsal_2018"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_inbody_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["inbody"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_freestyle_librelink_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        collection = self.connection.collections_pancreas["freestyle_librelink"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

   