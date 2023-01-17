from .results import StudyResults
from .functions import get_mealtracker_meals_results, get_mealtracker_fitbit_results


class ParticipantMealTrackerStudy:

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_id = study_info["test_id"]
        self.sensors = study_info["sensors"]
        self.start = study_info["timestamp_start"]
        self.end = study_info["timestamp_end"]


    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d") if self.end else "not finished"
        return f"{self.__class__} object (id: {self.test_id}, start_date:{init_date}, end_date:{end_date})"
        

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_id="all", sensors="all", fields="all"):
        fitbit_ids = [x["sensor_id"] for key, value in self.sensors.items() if key == "fitbit" for x in value]
        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_id, sensors, fields)


    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        test_ids = [self.test_id]
        collection = self.connection.collections_mealtracker["mealtracker"]
        return get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format)

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", specific_fitbit_id="all", sensors="all"):
        df_meals = self.get_meals_results(timestamp_start, timestamp_end, "all", specific_test_ids).astype("dataframe", True)
        results = []
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(row["timestamp_start"], row["timestamp_end"], specific_fitbit_id, sensors, fields)
            results += temp
        return StudyResults(results)


class ParticipantMealTrackerStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_id="all", sensors="all", fields="all"):
        fitbit_ids = [x["sensor_id"] for y in self.data for key, value in y.sensors.items() if key == "fitbit" for x in value]
        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_id, sensors, fields)

        
    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_mealtracker["mealtracker"]
        return get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format)

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", specific_fitbit_id="all", sensors="all"):
        df_meals = self.get_meals_results(timestamp_start, timestamp_end, "all", specific_test_ids).astype("dataframe", True)
        results = StudyResults([])
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(row["timestamp_start"], row["timestamp_end"], specific_fitbit_id, sensors, fields)
            results += temp
        return results

