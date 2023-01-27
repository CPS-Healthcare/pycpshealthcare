from .results import StudyResults

def get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields):
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


def get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format):
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


def get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, sensors, fields):
    if specific_fitbit_ids == "all":
            fitbit_ids = fitbit_ids
    else:
        if type(specific_fitbit_ids) == int:
            fitbit_ids = [specific_fitbit_ids]
        elif type(specific_fitbit_ids) == list:
            fitbit_ids = specific_fitbit_ids

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


def generate_narray_pipeline(sensor, id_match, bin_size=60, bin_unit="minute", timestamp_start=None, timestamp_end=None, dim=3):
    match_pipeline = {"$match": {"sensor": sensor, **id_match}}
    if timestamp_start or timestamp_end:
        match_pipeline["$match"]["timestamp"] = {}
        if timestamp_start:
            match_pipeline["$match"]["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            match_pipeline["$match"]["timestamp"]["$lte"] = timestamp_end
    pipeline=[
        match_pipeline,
        {"$group": {
            "_id": {"$dateTrunc": {"date": "$timestamp", "unit": bin_unit, "binSize": bin_size}},
            "count": {"$count": {}}
            }
        },
        {"$project": {  
            "_id": 0,
            "timestamp": "$_id",
            "count": 1
            }
        }
    ]
    group_pipe = {f"{oper}_{i}": {f"${oper}": {"$arrayElemAt": [ "$measures", i ]}}
                    for i in range(dim) for oper in ["avg", "min", "max"]
                 }
    pipeline[1]["$group"].update(group_pipe)
    project_pip = {f"{oper}_{i}": 1 for i in range(dim) for oper in ["avg", "min", "max"]}
    pipeline[2]["$project"].update(project_pip)
    return pipeline


def generate_pipeline(sensor, id_match, bin_size=60, bin_unit="minute", timestamp_start=None, timestamp_end=None):
    match_pipeline = {"$match": {"sensor": sensor, **id_match}}
    if timestamp_start or timestamp_end:
        match_pipeline["$match"]["timestamp"] = {}
        if timestamp_start:
            match_pipeline["$match"]["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            match_pipeline["$match"]["timestamp"]["$lte"] = timestamp_end
    pipeline=[
        match_pipeline,
        {"$group": {
            "_id": {"$dateTrunc": {"date": "$timestamp", "unit": bin_unit, "binSize": bin_size}},
            "avg": {"$avg": "$measures"},
            "max": {"$max": "$measures"},
            "min": {"$min": "$measures"},
            "count": {"$count": {}}
            }
        },
        {"$project": {  
            "_id": 0,
            "timestamp": "$_id",
            "avg": 1,
            "max": 1,
            "min": 1,
            "count": 1
            }
        }
    ]
    return pipeline


def get_mealtracker_fitbit_results_grouped(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, sensor, bin_size=60, bin_unit="minute"):
    if specific_fitbit_ids == "all":
            fitbit_ids = fitbit_ids
    else:
        if type(specific_fitbit_ids) == int:
            fitbit_ids = [specific_fitbit_ids]
        elif type(specific_fitbit_ids) == list:
            fitbit_ids = specific_fitbit_ids


    id_match = { "client_id": {"$in": fitbit_ids} }

    if sensor in ["hrm", "batt"]:
        pipeline = generate_pipeline(sensor, id_match, bin_size, bin_unit, timestamp_start, timestamp_end )
    elif sensor in ["accel", "gyro"]:
        pipeline = generate_narray_pipeline(sensor, id_match, bin_size, bin_unit, timestamp_start, timestamp_end, dim=3)

    return StudyResults(collection.aggregate(pipeline))