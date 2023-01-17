from .functions import get_pancreas_sensor_results


class ParticipantPancreasStudy:

    def __init__(self, study_info, connection):
        self.connection = connection
        self.study_info = study_info
        self.test_name = study_info["Nombre prueba"]
        self.test_id = study_info["test_id"]
        self.start = study_info["Desde"]
        self.end = study_info["Hasta"] 


    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.id}, start_date:{init_date}, end_date:{end_date})"
            

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["fitbit"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_empatica_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["empatica"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_equivital_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["equivital"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_fitnesspal_ejercicio_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["fitnesspal_ejercicio"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_fitnesspal_nutricion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["fitnesspal_nutricion"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_guardian_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["guardian"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_oscar_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["oscar"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)


class ParticipantPancreasStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["fitbit"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_empatica_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["empatica"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_equivital_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["equivital"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_fitnesspal_ejercicio_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["fitnesspal_ejercicio"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_fitnesspal_nutricion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["fitnesspal_nutricion"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def get_guardian_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["guardian"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_oscar_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas["oscar"]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
