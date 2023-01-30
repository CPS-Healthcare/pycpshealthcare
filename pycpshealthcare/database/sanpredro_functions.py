from .results import StudyResults

def get_sanpredro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields):
        if specific_test_ids == "all":
            test_ids = test_ids
        else:
            if str(specific_test_ids).isnumeric():
                test_ids = [int(specific_test_ids)]
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
