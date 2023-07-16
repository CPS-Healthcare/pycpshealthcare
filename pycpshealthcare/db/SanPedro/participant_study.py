from .functions import get_sanpedro_sensor_results, get_sanpedro_results_grouped, get_sanpedro_metadata_results
from .values import fitbit_v2_values, fitbit_values, freestyle_librelink_values, holter_values,\
      patrones_minsal_2018_values, alimentacion_values, inbody_values
#TODO: make grouped methods for both classes

class SanPedroStudyOcurrence:

    def __init__(self, study_info, connection):
        self.connection = connection
        # self.test_name = study_info["Nombre prueba"]
        self.test_id = study_info["test_id"]
        self.start = study_info["Desde"]
        self.end = study_info["Hasta"] 
        self.study_info = study_info


    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.test_id}, start_date:{init_date}, end_date:{end_date})"
            

    def get_fitbit_v2_metadata_results(self, metadata_type, timestamp_start=None, timestamp_end=None, test_ids="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections["SanPedro"]["fitbit_v2_metadata"]
        return get_sanpedro_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type, fields)


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, values="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections["SanPedro"][collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None,values="all", bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections["SanPedro"][collection_name]
        return get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
  
methods_parameters = {
    "get_fitbit_v2_results": _create_get_sensor_method(collection_name="fitbit_v2"),
    "get_fitbit_results": _create_get_sensor_method(collection_name="fitbit"),
    "get_holter_results": _create_get_sensor_method(collection_name="holter"),
    "get_alimentacion_results": _create_get_sensor_method(collection_name="alimentacion"),
    "get_patrones_minsal_2018_results": _create_get_sensor_method(collection_name="patrones_minsal_2018"),
    "get_inbody_results": _create_get_sensor_method(collection_name="inbody"),
    "get_freestyle_librelink_results": _create_get_sensor_method(collection_name="freestyle_librelink"),
}
grouped_methods_parameters = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method(collection_name="fitbit_v2", sensor_values=fitbit_v2_values),
    "get_fitbit_results_grouped": _create_get_sensor_grouped_method(collection_name="fitbit", sensor_values=fitbit_values),
    "get_holter_results_grouped": _create_get_sensor_grouped_method(collection_name="holter", sensor_values=holter_values),
    "get_alimentacion_results_grouped": _create_get_sensor_grouped_method(collection_name="alimentacion", sensor_values=alimentacion_values),
    "get_patrones_minsal_2018_results_grouped": _create_get_sensor_grouped_method(collection_name="patrones_minsal_2018", sensor_values=patrones_minsal_2018_values),
    "get_inbody_results_grouped": _create_get_sensor_grouped_method(collection_name="inbody", sensor_values=inbody_values),
    "get_freestyle_librelink_results_grouped": _create_get_sensor_grouped_method(collection_name="freestyle_librelink", sensor_values=freestyle_librelink_values),
}
for key, value in methods_parameters.items():
    setattr(SanPedroStudyOcurrence, key, value) 

for key, value in grouped_methods_parameters.items():
    setattr(SanPedroStudyOcurrence, key, value) 





class ParticipantSanPedroStudiesGroup:

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
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["SanPedro"]["fitbit_v2_metadata"]
        return get_sanpedro_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type, fields)


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, values="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections["SanPedro"][collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections["SanPedro"][collection_name]
        return get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    
methods_parameters_2 = {
    "get_fitbit_v2_results": _create_get_sensor_method_2(collection_name="fitbit_v2"),
    "get_fitbit_results": _create_get_sensor_method_2(collection_name="fitbit"),
    "get_holter_results": _create_get_sensor_method_2(collection_name="holter"),
    "get_alimentacion_results": _create_get_sensor_method_2(collection_name="alimentacion"),
    "get_patrones_minsal_2018_results": _create_get_sensor_method_2(collection_name="patrones_minsal_2018"),
    "get_inbody_results": _create_get_sensor_method_2(collection_name="inbody"),
    "get_freestyle_librelink_results": _create_get_sensor_method_2(collection_name="freestyle_librelink"),
}
grouped_methods_parameters_2 = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method_2(collection_name="fitbit_v2", sensor_values=fitbit_v2_values),
    "get_fitbit_results_grouped": _create_get_sensor_grouped_method_2(collection_name="fitbit", sensor_values=fitbit_values),
    "get_holter_results_grouped": _create_get_sensor_grouped_method_2(collection_name="holter", sensor_values=holter_values),
    "get_alimentacion_results_grouped": _create_get_sensor_grouped_method_2(collection_name="alimentacion", sensor_values=alimentacion_values),
    "get_patrones_minsal_2018_results_grouped": _create_get_sensor_grouped_method_2(collection_name="patrones_minsal_2018", sensor_values=patrones_minsal_2018_values),
    "get_inbody_results_grouped": _create_get_sensor_grouped_method_2(collection_name="inbody", sensor_values=inbody_values),
    "get_freestyle_librelink_results_grouped": _create_get_sensor_grouped_method_2(collection_name="freestyle_librelink", sensor_values=freestyle_librelink_values),
}
for key, value in methods_parameters_2.items():
    setattr(ParticipantSanPedroStudiesGroup, key, value) 

for key, value in grouped_methods_parameters_2.items():
    setattr(ParticipantSanPedroStudiesGroup, key, value) 