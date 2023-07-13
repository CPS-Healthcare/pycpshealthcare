from ..results import StudyResults


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


def get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, values, fields):
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

    if values == "all":
        pass
    else:
        query["sensor"] = {"$in": values}

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
    match_pipeline = {"$match": {"sensor": {"$in": sensor}, **id_match}}
    if timestamp_start or timestamp_end:
        match_pipeline["$match"]["timestamp"] = {}
        if timestamp_start:
            match_pipeline["$match"]["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            match_pipeline["$match"]["timestamp"]["$lte"] = timestamp_end
    pipeline=[
        match_pipeline,
        {"$group": {
            "_id": {"timestamp": {"$dateTrunc": {"date": "$timestamp", "unit": bin_unit, "binSize": bin_size}}, "client_id": "$client_id", "sensor": "$sensor"},
            "count": {"$count": {}}
            }
        },
        {"$project": {  
            "_id": 0,
            "timestamp": "$_id.timestamp",
            "client_id": "$_id.client_id",
            "count": 1,
            "sensor": "$_id.sensor"
            }
        }
    ]
    group_pipe = {}
    coordinates = ["x", "y", "z"]
    for oper in ["avg", "min", "max"]:
        for j, coord in enumerate(coordinates):
            group_pipe[f"{oper}_{j}"] = {f"${oper}": {"$cond": {"if": {"$isArray": "$measures"}, "then": {'$ifNull': [{"$arrayElemAt": ["$measures", j]}, 0]}, "else": "$measures" if j==0 else None}}}
            # group_pipe[f"{oper}"] = {f"${oper}": {"$cond": {"if": {"$isArray": "$measures"}, "then": None, "else": "$measures"}}}
            
                 
                   
    pipeline[1]["$group"].update(group_pipe)
    oper_full = [f"{oper}_{i}" for i, coord in enumerate(coordinates) for oper in ["avg", "min", "max"]] + ["avg", "min", "max"]
    project_pip_1 ={f"{oper}": 1 for oper in oper_full}
    pipeline[2]["$project"].update(project_pip_1)
    
    project_pip_2 = {
        "$project": {
            f"{oper}": [{"k": "$sensor", "v":  [f"${oper}_0", f"${oper}_1", f"${oper}_2"]}]
                for oper in ["avg", "min", "max"]
            }
        }
    project_pip_2["$project"].update({ 
        "timestamp": 1,
        "client_id": 1,
        "count": 1,
        "sensor": 1
        })
    project_pip_3 = {
        "$project": {
            f"{oper}": {"$arrayToObject": f"${oper}"} for oper in oper_full
            }
        }
    project_pip_3["$project"].update({ 
        "timestamp": 1,
        "client_id": 1,
        "count": 1,
        })
    project_pip_4 = {
        "$project": {
            f"{oper}.{i}": {
                "$filter": {
                    "input": f"${oper}.{i}",
                    "as": "d",
                    "cond": {
                        "$ne": ["$$d", None]
                        }
                    }
                } for i in sensor for oper in ["avg", "min", "max"]
           }
        }
    project_pip_4["$project"].update({
        "timestamp": 1,
        "client_id": 1,
        "count": 1,
        })
    project_pip_5 = {
        "$project": {  
           f"{oper}.{i}": {
            "$cond": {
                "if": {"$isArray": f"${oper}.{i}"},
                "then": {"$cond":{
                    "if": {"$eq": [{"$size": f"${oper}.{i}"}, 1]},
                    "then": {"$arrayElemAt": [f"${oper}.{i}", 0]},
                    "else": f"${oper}.{i}"
                }},
                "else": "$$REMOVE"
                }
            } for i in sensor for oper in ["avg", "min", "max"]
           }
        }
    project_pip_5["$project"].update({
        "timestamp": 1,
        "client_id": 1,
        "count": 1,
        })
    pipeline.append(project_pip_2)
    pipeline.append(project_pip_3)
    pipeline.append(project_pip_4)
    pipeline.append(project_pip_5)
    return pipeline


def generate_pipeline(sensor, id_match, bin_size=60, bin_unit="minute", timestamp_start=None, timestamp_end=None):
    match_pipeline = {"$match": {"sensor": {"$in": sensor}, **id_match}}
    if timestamp_start or timestamp_end:
        match_pipeline["$match"]["timestamp"] = {}
        if timestamp_start:
            match_pipeline["$match"]["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            match_pipeline["$match"]["timestamp"]["$lte"] = timestamp_end
    pipeline=[
        match_pipeline,
        {"$group": {
            "_id": {"timestamp": {"$dateTrunc": {"date": "$timestamp", "unit": bin_unit, "binSize": bin_size}}, "client_id": "$client_id"},
            "avg": {"$avg": "$measures"},
            "max": {"$max": "$measures"},
            "min": {"$min": "$measures"},
            "count": {"$count": {}}
            }
        },
        {"$project": {  
            "_id": 0,
            "timestamp": "$_id.timestamp",
            "client_id": "$_id.client_id",
            "avg": 1,
            "max": 1,
            "min": 1,
            "count": 1
            }
        },
        {"$sort": {
            "client_id": 1,
            "timestamp": 1,
            }
        }
    ]
    return pipeline


def get_mealtracker_fitbit_results_grouped(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, values, bin_size=60, bin_unit="minute"):
    if specific_fitbit_ids == "all":
            fitbit_ids = fitbit_ids
    else:
        if type(specific_fitbit_ids) == int:
            fitbit_ids = [specific_fitbit_ids]
        elif type(specific_fitbit_ids) == list:
            fitbit_ids = specific_fitbit_ids
    if values == "all": values = ["accel", "gyro", "hrm", "batt"]

    id_match = { "client_id": {"$in": fitbit_ids} }

    # if values in ["hrm", "batt"]:
    #     pipeline = generate_pipeline(values, id_match, bin_size, bin_unit, timestamp_start, timestamp_end )
    # elif values in ["accel", "gyro"]:
    pipeline = generate_narray_pipeline(values, id_match, bin_size, bin_unit, timestamp_start, timestamp_end, dim=3)

    return StudyResults(collection.aggregate(pipeline))