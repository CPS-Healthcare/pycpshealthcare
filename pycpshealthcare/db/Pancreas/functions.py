from ..results import StudyResults
from ..utils import generate_narray_pipeline, generate_vector_magnitude_pipeline, generate_vector_stats_magnitude_pipeline

def get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values, time_sorted=True):

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



def get_pancreas_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size=60, bin_unit="minute"):
    id_match = {"test_id": {"$in": test_ids}}
    pipeline = generate_narray_pipeline(id_match, bin_size, bin_unit, timestamp_start, timestamp_end, types=values)
    return StudyResults(collection.aggregate(pipeline))


def get_accel_vector_magnitude(test_ids, collection, timestamp_start, timestamp_end):
    id_match = {"test_id": {"$in": test_ids}}
    pipeline = generate_vector_magnitude_pipeline(id_match, timestamp_start, timestamp_end)
    return StudyResults(collection.aggregate(pipeline))


def get_accel_vector_magnitude_grouped(test_ids, collection, timestamp_start, timestamp_end, bin_size=60, bin_unit="minute"):
    id_match = {"test_id": {"$in": test_ids}}
    pipeline = generate_vector_stats_magnitude_pipeline(id_match, bin_size, bin_unit, timestamp_start, timestamp_end)
    return StudyResults(collection.aggregate(pipeline))