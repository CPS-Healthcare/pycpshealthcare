from .functions import get_chrononevado_sensor_results, get_chrononevado_results_grouped
from .values import cpet_environment_data_values, cpet_participant_data_values, \
cpet_raw_data_values, cpet_test_data_values, finapres_data_values, finapres_raw_data_values, spo2_raw_data_values
from datetime import datetime

# TODO: Test this classes!


class ChronoNevadoStudyOcurrence:

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_id = study_info["test_id"]
        self.start = datetime.fromisoformat(study_info["date"]) if type(study_info["date"])==str else study_info["date"]
        self.end = datetime.fromisoformat(study_info["date"]) if type(study_info["date"])==str else study_info["date"]
        self.study_info = study_info

    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.test_id}, start_date:{init_date}, end_date:{end_date})"
   


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, values="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections["ChronoNevado"][collection_name]
        return get_chrononevado_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, values="all", bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
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
    setattr(ChronoNevadoStudyOcurrence, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(ChronoNevadoStudyOcurrence, key, value)



class ParticipantChronoNevadoStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, test_id):
        for study in self.data:
            if study.test_id == test_id:
                return study
        return None


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"):
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["ChronoNevado"][collection_name]
        return get_chrononevado_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        test_ids = [x.test_id for x in self.data]
        if test_ids == "all":
            test_ids = test_ids
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

methods_parameters_2 = {
    "get_cpet_raw_data": _create_get_sensor_method_2(collection_name="CpetRawData"),
    "get_cpet_participant_data": _create_get_sensor_method_2(collection_name="CpetParticipantData"),
    "get_cpet_test_data": _create_get_sensor_method_2(collection_name="CpetTestData"),
    "get_cpet_environment_data": _create_get_sensor_method_2(collection_name="CpetEnvironmentData"),
    "get_finapres_data": _create_get_sensor_method_2(collection_name="FinapresData"),
    "get_finapres_raw_data": _create_get_sensor_method_2(collection_name="FinapresRawData"),
    "get_spo2_raw_data": _create_get_sensor_method_2(collection_name="Spo2RawData"),
}

grouped_methods_parameters_2 = {
    "get_cpet_raw_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="CpetRawData",
        sensor_values=cpet_raw_data_values
        ),
    "get_cpet_participant_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="CpetParticipantData",
        sensor_values=cpet_participant_data_values
        ),
    "get_cpet_test_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="CpetTestData",
        sensor_values=cpet_test_data_values
        ),
    "get_cpet_environment_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="CpetEnvironmentData",
        sensor_values=cpet_environment_data_values
        ),
    "get_finapres_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="FinapresData",
        sensor_values=finapres_data_values
        ),
    "get_finapres_raw_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="FinapresRawData",
        sensor_values=finapres_raw_data_values,
        ),
    "get_spo2_raw_data_grouped": _create_get_sensor_grouped_method_2(
        collection_name="Spo2RawData",
        sensor_values=spo2_raw_data_values),
}

for key, value in methods_parameters_2.items():
    setattr(ParticipantChronoNevadoStudiesGroup, key, value)

for key, value in grouped_methods_parameters_2.items():
    setattr(ParticipantChronoNevadoStudiesGroup, key, value)