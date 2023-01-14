import pandas as pd
from .results import StudyResults

class ParticipantMealTrackerStudy:

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_id = study_info["test_id"]
        self.sensors = study_info["sensors"]
        self.start = study_info["timestamp_start"]
        self.end = study_info["timestamp_end"]

    # def __str__(self) -> str:
    #     return "temp"

    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d") if self.end else "not finished"
        return f"{self.__class__} object (id: {self.test_id}, start_date:{init_date}, end_date:{end_date})"
        

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_id="all", sensors="all", fields="all"):
        if specific_fitbit_id == "all":
            fitbit_ids = [x["sensor_id"] for key, value in self.sensors.items() if key == "fitbit" for x in value]
        else:
            if type(specific_fitbit_id) == int:
                fitbit_ids = [specific_fitbit_id]
            elif type(specific_fitbit_id) == list:
                fitbit_ids = specific_fitbit_id

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
                "client_id": {"$in": fitbit_ids}
            }

        if sensors == "all":
            pass
        else:
            query["sensor"] = {"$in": sensors}

        if timestamp_start or timestamp_end:
            query["timestamp"] = {}
            if timestamp_start:
                query["timestamp"]["$gte"] = timestamp_start
            if timestamp_end:
                query["timestamp"]["$lte"] = timestamp_end

        collection = self.connection.collections_mealtracker["realtimefitbit"]
        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))
    
    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        if specific_test_ids == "all":
            test_ids = [self.test_id]
        else:
            if type(specific_test_ids) == int:
                test_ids = [specific_test_ids]
            elif type(specific_test_ids) == list:
                test_ids = specific_test_ids

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

        if timestamp_start or timestamp_end:
            if timestamp_start:
                query["records.timestamp_start"] = {"$gte": timestamp_start}
            if timestamp_end:
                query["records.timestamp_end"] = {"$lte": timestamp_end}
                
        if ouput_format in ["unwinded"]:
            collection = self.connection.collections_mealtracker["mealtracker"]
            pipeline = [{"$unwind":  {"path": "$records"}}, {"$match": query}]
            if projection: pipeline.append({"$project": projection})
            return StudyResults(collection.aggregate(pipeline))

        elif ouput_format == "original":
            parameters = {"filter": query}
            if projection: parameters["projection"] = projection
            return StudyResults(collection.find(**parameters))


class MealTrackerStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_id="all", sensors="all", fields="all"):
        if specific_fitbit_id == "all":
            fitbit_ids = [x["sensor_id"] for y in self.data for key, value in y.sensors.items() if key == "fitbit" for x in value]
        else:
            if type(specific_fitbit_id) == int:
                fitbit_ids = [specific_fitbit_id]
            elif type(specific_fitbit_id) == list:
                fitbit_ids = specific_fitbit_id

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
                "client_id": {"$in": fitbit_ids}
            }

        if sensors == "all":
            pass
        else:
            query["sensor"] = {"$in": sensors}

        if timestamp_start or timestamp_end:
            query["timestamp"] = {}
            if timestamp_start:
                query["timestamp"]["$gte"] = timestamp_start
            if timestamp_end:
                query["timestamp"]["$lte"] = timestamp_end
        collection = self.connection.collections_mealtracker["realtimefitbit"]
        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))


    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        if specific_test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if type(specific_test_ids) == int:
                test_ids = [specific_test_ids]
            elif type(specific_test_ids) == list:
                test_ids = specific_test_ids

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

        if timestamp_start or timestamp_end:
            if timestamp_start:
                query["records.timestamp_start"] = {"$gte": timestamp_start}
            if timestamp_end:
                query["records.timestamp_end"] = {"$lte": timestamp_end}

        if ouput_format in ["unwinded"]:
            collection = self.connection.collections_mealtracker["mealtracker"]
            pipeline = [{"$unwind":  {"path": "$records"}}, {"$match": query}]
            if projection: pipeline.append({"$project": projection})
            return StudyResults(collection.aggregate(pipeline))

        elif ouput_format == "original":
            parameters = {"filter": query}
            if projection: parameters["projection"] = projection
            return StudyResults(collection.find(**parameters))

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", specific_fitbit_id="all", sensors="all"):
        df_meals = self.get_meals_results(timestamp_start, timestamp_end, "all", specific_test_ids).astype("dataframe", True)
        results = []
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(row["timestamp_start"],row["timestamp_end"], specific_fitbit_id, sensors, fields)
            results += temp
        return StudyResults(results)


