

def generate_narray_pipeline(id_match, bin_size=60, bin_unit="minute", timestamp_start=None, timestamp_end=None, types=[]):
    match_pipeline = {"$match": {**id_match}}
    if timestamp_start or timestamp_end:
        match_pipeline["$match"]["timestamp"] = {}
        if timestamp_start:
            match_pipeline["$match"]["timestamp"]["$gte"] = timestamp_start
        if timestamp_end:
            match_pipeline["$match"]["timestamp"]["$lte"] = timestamp_end
    pipeline=[
        match_pipeline,
        {"$group": {
            "_id": {"timestamp": {"$dateTrunc": {"date": "$timestamp", "unit": bin_unit, "binSize": bin_size}}, "test_id": "$test_id"},
            "count": {"$count": {}},
            }
        },
        {"$project": {  
            "_id": 0,
            "timestamp": "$_id.timestamp",
            "test_id": "$_id.test_id",
            "count": 1,
            },
        },
        {"$sort": {
            "test_id": 1,
            "timestamp": 1,
            }
        }
    ]
    group_pipe = {f"{oper}_{i}": {f"${oper}": f"$values.{i}"}
                    for i in types for oper in ["avg", "min", "max"]
                 }
    pipeline[1]["$group"].update(group_pipe)
    # project_pip = {f"{oper}_{i}": 1 for i in types for oper in ["avg", "min", "max"]}
    project_pip = {f"{oper}": {i: f"${oper}_{i}"  for i in types}  for oper in ["avg", "min", "max"]}
    pipeline[2]["$project"].update(project_pip)
    return pipeline