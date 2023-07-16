from ..results import StudyResults
from ..utils import generate_narray_pipeline


def get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, ouput_format="unwinded"):


    projection = {
        "_id": 0,
        "test_id": 1,
        "values": 1,
    }  

    query = {
        "test_id": {"$in": test_ids}
    }

    if timestamp_start or timestamp_end:
        if timestamp_start:
            query["values.timestamp_start"] = {"$gte": timestamp_start}
        if timestamp_end:
            query["values.timestamp_end"] = {"$lte": timestamp_end}

    if ouput_format in ["unwinded"]:
        pipeline = [{"$unwind":  {"path": "$values"}}, {"$match": query}]
        if projection:
            if "_id" not in projection.keys():
                projection["_id"] = 0
        else:
            projection = {"_id": 0}
        pipeline.append({"$project": projection})
        print(pipeline)
        return StudyResults(collection.aggregate(pipeline))

    elif ouput_format == "original":
        parameters = {"filter": query}
        if projection:
            if "_id" not in projection.keys():
                projection["_id"] = 0
        else:
            projection = {"_id": 0}
        pipeline.append({"$project": projection})
        return StudyResults(collection.find(**parameters))


def get_mealtracker_fitbit_results(test_ids, collection, timestamp_start, timestamp_end, values, time_sorted=True):

    projection = {
        "_id": 0,
        "timestamp": 1,
        "test_id": 1,
        "values": 1,
    }       

    query = {
        "test_id": {"$in": test_ids}
    }

    if values == "all":
        pass
    elif type(values) == str:
        query[f"values.{values}"] = {"$exists": True}
        del projection["values"]
        projection[f"values.{values}"] = 1
    else:
        query["$or"] = []
        del projection["values"]
        for sensor in values:
            query["$or"].append({f"values.{sensor}": {"$exists": True}})
            projection[f"values.{sensor}"] = 1

    if timestamp_start or timestamp_end:
        query["timestamp"] = {}
        if timestamp_start:
            query["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            query["timestamp"]["$lte"] = timestamp_end

    parameters = {"filter": query}
    if projection: parameters["projection"] = projection
    if time_sorted:
        return StudyResults(collection.find(**parameters).sort([["timestamp", 1]]))
    else:
        return StudyResults(collection.find(**parameters))



def get_mealtracker_fitbit_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size=60, bin_unit="minute"):
    id_match = {"test_id": {"$in": test_ids}}
    pipeline = generate_narray_pipeline(id_match, bin_size, bin_unit, timestamp_start, timestamp_end, types=values)
    return StudyResults(collection.aggregate(pipeline))