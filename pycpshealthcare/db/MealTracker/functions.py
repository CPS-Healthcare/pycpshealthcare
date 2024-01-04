from ..results import StudyResults
from ..utils import generate_narray_pipeline


def get_mealtracker_meals_results(
    collection, test_ids, timestamp_start, timestamp_end, ouput_format="unwinded"
):
    """
    A function that generates a MongoDB query from arguments for the specified collection.

    :return: An iterable with the database query results.
    :rtype: pycpshealthcare.db.results.StudyResults

    :param test_ids: A list of test ids to query.
    :type test_ids: list<int>

    :param collection: The collection of the sensor to query.
    :type collection:  pymongo.collection.Collection

    :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
    :type timestamp_start:  datetime.datetime|None, optional

    :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
    :type timestamp_end:  datetime.datetime|None, optional

    :param ouput_format: unwinded|original
    :type ouput_format:  str

    """

    projection = {
        "_id": 0,
        "test_id": 1,
        "values": 1,
    }

    query = {"test_id": {"$in": test_ids}}

    if timestamp_start or timestamp_end:
        if timestamp_start:
            query["values.timestamp_start"] = {"$gte": timestamp_start}
        if timestamp_end:
            query["values.timestamp_end"] = {"$lte": timestamp_end}

    if ouput_format in ["unwinded"]:
        pipeline = [{"$unwind": {"path": "$values"}}, {"$match": query}]
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


def get_mealtracker_fitbit_results(
    test_ids, collection, timestamp_start, timestamp_end, values, time_sorted=True
):
    """
    A function that generates a MongoDB query from arguments for the specified collection.

    :return: An iterable with the database query results.
    :rtype: pycpshealthcare.db.results.StudyResults

    :param test_ids: A list of test ids to query.
    :type test_ids: list<int>

    :param collection: The collection of the sensor to query.
    :type collection:  pymongo.collection.Collection

    :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
    :type timestamp_start:  datetime.datetime|None, optional

    :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
    :type timestamp_end:  datetime.datetime|None, optional

    :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
    :type values: str|list<str>|None, optional

    """

    projection = {
        "_id": 0,
        "timestamp": 1,
        "test_id": 1,
        "values": 1,
    }

    query = {"test_id": {"$in": test_ids}}

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


def get_mealtracker_fitbit_results_grouped(
    test_ids, collection, timestamp_start, timestamp_end, values, bin_size=60, bin_unit="minute"
):
    """
    :return: an iterable with the query results
    :rtype: pycpshealthcare.db.results.StudyResults

    :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
    :type timestamp_start:  datetime.datetime|None, optional

    :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
    :type timestamp_end:  datetime.datetime|None, optional

    :param test_ids: The ids of the tests to be queried, defaults to "all" that brings data of all the test ids.
    :type test_ids: int|list<int>|None, optional

    :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
    :type values: str|list<str>|None, optional

    :param bin_size: The width of the mobile window, defaults to 60.
    :type bin_size: int, optional

    :param bin_unit: The unit of the mobile window, defaults to minute. Options are minute, hour, day.
    :type bin_unit: str, optional
    """
    id_match = {"test_id": {"$in": test_ids}}
    pipeline = generate_narray_pipeline(
        id_match, bin_size, bin_unit, timestamp_start, timestamp_end, types=values
    )
    return StudyResults(collection.aggregate(pipeline))
