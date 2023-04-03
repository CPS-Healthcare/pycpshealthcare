from .results import StudyResults
from .participant_info import ParticipantInfo
from .sanpedro_functions import get_sanpredro_sensor_results, get_sanpedro_results_grouped


class SanPedroStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Pancreas").astype("participant")
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["Pancreas"]]

    def get_fitbit_v2_results_grouped(self, measure, timestamp_start=None, timestamp_end=None, specific_test_ids="all",  bin_size=60, bin_unit="minute"):
        test_ids = self.test_ids
        collection = self.connection.collections_sanpedro["fitbit_v2"]
        return get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, measure, bin_size, bin_unit)
    

def create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", fields="all"):
        test_ids = self.test_ids
        collection = self.connection.collections_sanpedro[collection_name]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, fields)
    return get_sensor_results


def create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections_pancreas[collection_name]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    

methods_parameters = {
    "get_fitbit_v2_results": create_get_sensor_method(collection_name="fitbit_v2"),
    "get_fitbit_results": create_get_sensor_method(collection_name="fitbit"),
    "get_alimentacion_results": create_get_sensor_method(collection_name="alimentacion"),
    "get_patrones_minsal_2018_results": create_get_sensor_method(collection_name="patrones_minsal_2018"),
    "get_inbody_results": create_get_sensor_method(collection_name="inbody"),
    "get_freestyle_librelink_results": create_get_sensor_method(collection_name="freestyle_librelink"),
}
for key, value in methods_parameters.items():
    setattr(SanPedroStudy, key, value)