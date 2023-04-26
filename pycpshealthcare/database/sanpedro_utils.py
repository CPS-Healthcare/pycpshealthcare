from .sanpedro_functions import get_sanpedro_sensor_results, get_sanpedro_results_grouped


class ParticipantSanPedroStudy:

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
            

    def get_fitbit_v2_results_grouped(self, measure, timestamp_start=None, timestamp_end=None, specific_test_id="all",  bin_size=60, bin_unit="minute"):
        if specific_test_id == "all":
            test_ids = self.test_id
        else:
            test_ids = specific_test_id

        collection = self.connection.collections_sanpedro["fitbit_v2"]
        return get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, measure, bin_size, bin_unit)


def create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    return get_sensor_results


def create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections_sanpedro[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped
  
methods_parameters = {
    "get_fitbit_v2_results": create_get_sensor_method(collection_name="fitbit_v2"),
    "get_fitbit_results": create_get_sensor_method(collection_name="fitbit"),
    "get_holter_results": create_get_sensor_method(collection_name="holter"),
    "get_alimentacion_results": create_get_sensor_method(collection_name="alimentacion"),
    "get_patrones_minsal_2018_results": create_get_sensor_method(collection_name="patrones_minsal_2018"),
    "get_inbody_results": create_get_sensor_method(collection_name="inbody"),
    "get_freestyle_librelink_results": create_get_sensor_method(collection_name="freestyle_librelink"),
}
for key, value in methods_parameters.items():
    setattr(ParticipantSanPedroStudy, key, value) 





class ParticipantSanPedroStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None


def create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    return get_sensor_results


def create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections_pancreas[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    
methods_parameters_2 = {
    "get_fitbit_v2_results": create_get_sensor_method_2(collection_name="fitbit_v2"),
    "get_fitbit_results": create_get_sensor_method_2(collection_name="fitbit"),
    "get_holter_results": create_get_sensor_method_2(collection_name="holter"),
    "get_alimentacion_results": create_get_sensor_method_2(collection_name="alimentacion"),
    "get_patrones_minsal_2018_results": create_get_sensor_method_2(collection_name="patrones_minsal_2018"),
    "get_inbody_results": create_get_sensor_method_2(collection_name="inbody"),
    "get_freestyle_librelink_results": create_get_sensor_method_2(collection_name="freestyle_librelink"),
}
for key, value in methods_parameters_2.items():
    setattr(ParticipantSanPedroStudiesGroup, key, value) 