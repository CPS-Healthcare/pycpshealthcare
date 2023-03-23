from .sanpredro_functions import get_sanpredro_sensor_results, get_sanpedro_fitbit_v2_results_grouped

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
            

    def get_fitbit_v2_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["fitbit_v2"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["fitbit"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_alimentacion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["alimentacion"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_patrones_minsal_2018_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["patrones_minsal_2018"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_inbody_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["inbody"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_freestyle_librelink_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_sanpedro["freestyle_librelink"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_fitbit_v2_results_grouped(self, measure, timestamp_start=None, timestamp_end=None, specific_test_id="all",  bin_size=60, bin_unit="minute"):
        if specific_test_id == "all":
            test_ids = self.test_id
        else:
            test_ids = specific_test_id

        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_sanpedro_fitbit_v2_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, measure, bin_size, bin_unit)

   

class ParticipantSanPedroStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None

    def get_fitbit_v2_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["fitbit_v2"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["fitbit"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_alimentacion_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["alimentacion"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_patrones_minsal_2018_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["patrones_minsal_2018"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_inbody_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["inbody"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

    def get_freestyle_librelink_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_sanpedro["freestyle_librelink"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

  