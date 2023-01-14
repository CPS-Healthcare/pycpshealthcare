from .results import StudyResults

def get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields):
        if specific_test_id == "all":
            test_ids = test_ids
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

        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))


def get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format):
    if specific_test_ids == "all":
        test_ids = test_ids
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
        pipeline = [{"$unwind":  {"path": "$records"}}, {"$match": query}]
        if projection: pipeline.append({"$project": projection})
        return StudyResults(collection.aggregate(pipeline))

    elif ouput_format == "original":
        parameters = {"filter": query}
        if projection: parameters["projection"] = projection
        return StudyResults(collection.find(**parameters))


def get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_id, sensors, fields):
    if specific_fitbit_id == "all":
            fitbit_ids = fitbit_ids
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
    parameters = {"filter": query}
    if projection: parameters["projection"] = projection
    return StudyResults(collection.find(**parameters))