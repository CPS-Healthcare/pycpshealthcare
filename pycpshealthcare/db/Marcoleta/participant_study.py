from .functions import get_sanpedro_sensor_results, get_sanpedro_results_grouped


class ParticipantMarcoletaStudy:

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
            

    def get_fitbit_v2_results_grouped(self, measure, timestamp_start=None, timestamp_end=None, specific_test_id="all",  bin_size=60, bin_unit="minute"):
        if specific_test_id == "all":
            test_ids = self.test_id
        else:
            test_ids = specific_test_id

        collection = self.connection.collections_marcoleta["fitbit_v2"]
        return get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, measure, bin_size, bin_unit)


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_marcoleta[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if specific_test_ids == "all":
            test_ids = self.test_ids
        else:
            test_ids = specific_test_ids
        if values == "all":
            values = sensor_values 
        collection = self.connection.collections_marcoleta[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped
  
methods_parameters = {
    "get_fitbit_v2_results": _create_get_sensor_method(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method(collection_name="holter"),
    "get_autoreports_results": _create_get_sensor_method(collection_name="autoreports"),
}
for key, value in methods_parameters.items():
    setattr(ParticipantMarcoletaStudy, key, value) 





class ParticipantMarcoletaStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_marcoleta[collection_name]
        return get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
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
    "get_fitbit_v2_results": _create_get_sensor_method_2(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method_2(collection_name="holter"),
    "get_autoreports_results": _create_get_sensor_method_2(collection_name="autoreports"),
}
for key, value in methods_parameters_2.items():
    setattr(ParticipantMarcoletaStudiesGroup, key, value) 