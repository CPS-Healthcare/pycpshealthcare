from ..results import StudyResults
from ..utils import generate_narray_pipeline


def get_marcoleta_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, time_sorted=True):

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
    if projection:
        parameters["projection"] = projection
    if time_sorted:
        return StudyResults(collection.find(**parameters).sort([["timestamp", 1]]))
    else:
        return StudyResults(collection.find(**parameters))


def get_marcoleta_metadata_results(test_ids, collection, timestamp_start, timestamp_end, metadata_type):

    projection = {
        "_id": 0,
    }

    query = {
            "test_id": {"$in": test_ids}
        }


    query[f"metadata_type"] = metadata_type

    if timestamp_start or timestamp_end:
        query["startTime"] = {}
        if timestamp_start:
            query["startTime"]["$gte"] = timestamp_start
        if timestamp_end:
            query["startTime"]["$lte"] = timestamp_end

    parameters = {"filter": query}
    if projection:
        parameters["projection"] = projection
    return StudyResults(collection.find(**parameters))



def get_marcoleta_sensor_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size=60, bin_unit="minute"):

    id_match = {"test_id": {"$in": test_ids}}

    pipeline = generate_narray_pipeline(id_match, bin_size, bin_unit, timestamp_start, timestamp_end, types=values)
    print(pipeline)
    return StudyResults(collection.aggregate(pipeline))