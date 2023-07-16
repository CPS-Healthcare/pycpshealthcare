from ..results import StudyResults
from ..participant_info import ParticipantInfo
from .functions import get_chrononevado_sensor_results, \
    get_chrononevado_results_grouped

from .values import cpet_environment_data_values, cpet_participant_data_values, \
cpet_raw_data_values, cpet_test_data_values, finapres_data_values, finapres_raw_data_values, spo2_raw_data_values


class ChronoNevadoStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["ChronoNevado"]]


    # def get_empatica_accel_vector_magnitude(self, timestamp_start=None, timestamp_end=None, test_ids="all"):
    #     collection = self.connection.collections["ChronoNevado"]["empatica"]
    #     return get_accel_vector_magnitude(self.test_ids, collection, timestamp_start, timestamp_end, test_ids)
    

    # def get_empatica_accel_vector_magnitude_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", bin_size=60, bin_unit="minute"):
    #     collection = self.connection.collections["ChronoNevado"]["empatica"]
    #     return get_accel_vector_magnitude_grouped(self.test_ids, collection, timestamp_start, timestamp_end, test_ids, bin_size, bin_unit)



def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["ChronoNevado"][collection_name]
        return get_chrononevado_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections["ChronoNevado"][collection_name]
        return get_chrononevado_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    

methods_parameters = {
    "get_cpet_raw_data": _create_get_sensor_method(collection_name="CpetRawData"),
    "get_cpet_participant_data": _create_get_sensor_method(collection_name="CpetParticipantData"),
    "get_cpet_test_data": _create_get_sensor_method(collection_name="CpetTestData"),
    "get_cpet_environment_data": _create_get_sensor_method(collection_name="CpetEnvironmentData"),
    "get_finapres_data": _create_get_sensor_method(collection_name="FinapresData"),
    "get_finapres_raw_data": _create_get_sensor_method(collection_name="FinapresRawData"),
    "get_spo2_raw_data": _create_get_sensor_method(collection_name="Spo2RawData"),
}

grouped_methods_parameters = {
    "get_cpet_raw_data_grouped": _create_get_sensor_grouped_method(
        collection_name="CpetRawData",
        sensor_values=cpet_raw_data_values
        ),
    "get_cpet_participant_data_grouped": _create_get_sensor_grouped_method(
        collection_name="CpetParticipantData",
        sensor_values=cpet_participant_data_values
        ),
    "get_cpet_test_data_grouped": _create_get_sensor_grouped_method(
        collection_name="CpetTestData",
        sensor_values=cpet_test_data_values
        ),
    "get_cpet_environment_data_grouped": _create_get_sensor_grouped_method(
        collection_name="CpetEnvironmentData",
        sensor_values=cpet_environment_data_values
        ),
    "get_finapres_data_grouped": _create_get_sensor_grouped_method(
        collection_name="FinapresData",
        sensor_values=finapres_data_values
        ),
    "get_finapres_raw_data_grouped": _create_get_sensor_grouped_method(
        collection_name="FinapresRawData",
        sensor_values=finapres_raw_data_values,
        ),
    "get_spo2_raw_data_grouped": _create_get_sensor_grouped_method(
        collection_name="Spo2RawData",
        sensor_values=spo2_raw_data_values),
}

for key, value in methods_parameters.items():
    setattr(ChronoNevadoStudy, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(ChronoNevadoStudy, key, value)
