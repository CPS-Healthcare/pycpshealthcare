from .results import StudyResults


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
        if specific_test_id == "all":
            test_ids = [self.test_id]
        else:
            if type(specific_test_id) == int:
                test_ids = [specific_test_id]
            elif type(specific_test_id) == list:
                test_ids = specific_test_id

        if fields == "all":
            projection = ""
        else:
            if type(fields) == str:
                projection = [fields]
            elif type(fields) == list:
                projection = fields
            projection = {x: 1 for x in projection}
            if "_id" not in projection.keys():
                projection["_id"] = 0

        query = {
                "test_id": {"$in": test_ids}
            }

        if sensors == "all":
            pass
        else:
            for sensor in sensors:
                query[f"values.{sensor}"] = {"$exists": True}

        if timestamp_start or timestamp_end:
            query["timestamp"] = {}
            if timestamp_start:
                query["timestamp"]["$gte"] = timestamp_start
            if timestamp_end:
                query["timestamp"]["$lte"] = timestamp_end

        collection = self.connection.collections_pancreas["fitbit"]
        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))

class PancreasStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("fitbit", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_empatica_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("empatica", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_equivital_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("equivital", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_fitnesspal_ejercicio_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("fitnesspal_ejercicio", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_fitnesspal_nutricion_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("fitnesspal_nutricion", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_guardian_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("guardian", timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    
    def get_oscar_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        return self._get_sensor_results("oscar", timestamp_start, timestamp_end, specific_test_id, sensors, fields)

    def _get_sensor_results(self, collection_name, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        if specific_test_id == "all":
            test_ids = [x.test_id for x in self.data]
            print(test_ids)
        else:
            if type(specific_test_id) == int:
                test_ids = [specific_test_id]
            elif type(specific_test_id) == list:
                test_ids = specific_test_id

        if fields == "all":
            projection = ""
        else:
            if type(fields) == str:
                projection = [fields]
            elif type(fields) == list:
                projection = fields
            projection = {x: 1 for x in projection}
            if "_id" not in projection.keys():
                projection["_id"] = 0

        query = {
                "test_id": {"$in": test_ids}
            }

        if sensors == "all":
            pass
        else:
            for sensor in sensors:
                query[f"values.{sensor}"] = {"$exists": True}

        if timestamp_start or timestamp_end:
            query["timestamp"] = {}
            if timestamp_start:
                query["timestamp"]["$gte"] = timestamp_start
            if timestamp_end:
                query["timestamp"]["$lte"] = timestamp_end

        collection = self.connection.collections_pancreas[collection_name]
        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))