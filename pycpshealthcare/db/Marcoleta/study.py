from ..results import StudyResults
from ..participant_info import ParticipantInfo
from .functions import get_marcoleta_sensor_results, get_marcoleta_results_grouped, get_marcoleta_metadata_results
from .values import fitbit_v2_values, holter_values, autoreportes_values

class MarcoletaStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Marcoleta").astype("participant")
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["Marcoleta"]]

    def get_fitbit_v2_metadata_results(self, metadata_type, timestamp_start=None, timestamp_end=None, test_ids="all", fields="all"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections_marcoleta["fitbit_v2_metadata"]
        return get_marcoleta_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type, fields)
    

def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", fields="all"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections_marcoleta[collection_name]
        return get_marcoleta_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections_marcoleta[collection_name]
        return get_marcoleta_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    

methods_parameters = {
    "get_fitbit_v2_results": _create_get_sensor_method(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method(collection_name="holter"),
    "get_autoreports_results":  _create_get_sensor_method(collection_name="autoreports")
}

grouped_methods_parameters = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitbit_v2",
        sensor_values=fitbit_v2_values
        ),
    "get_holter_results_grouped": _create_get_sensor_grouped_method(
        collection_name="holter",
        sensor_values=holter_values
        ),
    "get_autoreports_results_grouped": _create_get_sensor_grouped_method(
        collection_name="autoreports",
        sensor_values=autoreportes_values
        ),
}

for key, value in methods_parameters.items():
    setattr(MarcoletaStudy, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(MarcoletaStudy, key, value)