from .functions import get_marcoleta_sensor_results, get_marcoleta_sensor_results_grouped, get_marcoleta_metadata_results
from .values import fitbit_v2_values, holter_values

class MarcoletaStudyOcurrence:

    def __init__(self, study_info, connection):
        self.connection = connection
        # self.test_name = study_info["Nombre prueba"]
        self.test_id = study_info["test_id"]
        self.start = study_info["FECHA INICIO"]
        self.end = study_info["FECHA RETIRO"] 
        self.study_info = study_info


    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.test_id}, start_date:{init_date}, end_date:{end_date})"
            

    def get_fitbit_v2_results_grouped(self, measure, timestamp_start=None, timestamp_end=None,  bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
        collection = self.connection.collections["Marcoleta"]["fitbit_v2"]
        return get_marcoleta_sensor_results_grouped(test_ids, collection, timestamp_start, timestamp_end, measure, bin_size, bin_unit)
    

    def get_fitbit_v2_metadata_results(self, metadata_type, timestamp_start=None, timestamp_end=None, test_ids="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections["Marcoleta"]["fitbit_v2_metadata"]
        return get_marcoleta_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type, fields)


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, values="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, values="all", bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
  
methods_parameters = {
    "get_fitbit_v2_results": _create_get_sensor_method(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method(collection_name="holter"),
    "get_autoreports_results": _create_get_sensor_method(collection_name="autoreports"),
}
grouped_methods_parameters = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method(collection_name="fitbit_v2", sensor_values=fitbit_v2_values),
    "get_holter_results_grouped": _create_get_sensor_grouped_method(collection_name="holter", sensor_values=holter_values),
}
for key, value in methods_parameters.items():
    setattr(MarcoletaStudyOcurrence, key, value) 

for key, value in grouped_methods_parameters.items():
    setattr(MarcoletaStudyOcurrence, key, value) 





class ParticipantMarcoletaStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None

    def get_fitbit_v2_metadata_results(self, metadata_type, timestamp_start=None, timestamp_end=None, test_ids="all", fields="all"):
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Marcoleta"]["fitbit_v2_metadata"]
        return get_marcoleta_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type, fields)


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", fields="all"):
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    
methods_parameters_2 = {
    "get_fitbit_v2_results": _create_get_sensor_method_2(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method_2(collection_name="holter"),
    "get_autoreports_results": _create_get_sensor_method_2(collection_name="autoreports"),
}
grouped_methods_parameters_2 = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method_2(collection_name="fitbit_v2", sensor_values=fitbit_v2_values),
    "get_holter_results_grouped": _create_get_sensor_grouped_method_2(collection_name="holter", sensor_values=holter_values),
}
for key, value in methods_parameters_2.items():
    setattr(ParticipantMarcoletaStudiesGroup, key, value) 
for key, value in grouped_methods_parameters_2.items():
    setattr(ParticipantMarcoletaStudiesGroup, key, value) 