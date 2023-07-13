from ..results import StudyResults
from ..utils import generate_narray_pipeline


def get_sanpedro_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields, time_sorted=True):
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
    if projection:
        parameters["projection"] = projection
    if time_sorted:
        return StudyResults(collection.find(**parameters).sort([["timestamp", 1]]))
    else:
        return StudyResults(collection.find(**parameters))


def get_sanpedro_metadata_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, metadata_type, fields):
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



def get_sanpedro_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size=60, bin_unit="minute"):
    if specific_test_ids == "all":
        test_ids = test_ids
    else:
        if type(specific_test_ids) == int:
            test_ids = [specific_test_ids]
        elif type(specific_test_ids) == list:
            test_ids = specific_test_ids

    id_match = {"test_id": {"$in": test_ids}}

    pipeline = generate_narray_pipeline(id_match, bin_size, bin_unit, timestamp_start, timestamp_end, types=values)
    print(pipeline)
    return StudyResults(collection.aggregate(pipeline))