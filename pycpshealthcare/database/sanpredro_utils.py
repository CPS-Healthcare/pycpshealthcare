from .sanpredro_functions import get_sanpredro_sensor_results

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
            

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["fitbit"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_alimentacion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["alimentacion"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_patrones_minsal_2018_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["patrones_minsal_2018"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_inbody_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["inbody"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_freestyle_librelink_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["freestyle_librelink"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

   

class ParticipantSanPedroStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["fitbit"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_alimentacion_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["alimentacion"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_patrones_minsal_2018_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["patrones_minsal_2018"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    
    def get_inbody_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["inbody"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

    def get_freestyle_librelink_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["freestyle_librelink"]
        return get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)

  