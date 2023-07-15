from ..participant_info import ParticipantInfo
from ..results import StudyResults
import pandas as pd
from .functions import get_mealtracker_meals_results, get_mealtracker_fitbit_results,\
    get_mealtracker_fitbit_results_grouped

class MealTrackerStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="MealTracker").astype("Participant")

        
    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, fitbit_ids="all", values="all", fields="all"):
        if fitbit_ids == "all":
            fitbit_ids = [y["sensor_id"] for p in self.participants for t in p.studies["MealTracker"] for key, value in t.sensors.items() for y in value if key == "fitbit"]
        else:
            if str(fitbit_ids).isnumeric():
                    fitbit_ids = [int(fitbit_ids)]
            elif type(fitbit_ids) == list:
                fitbit_ids = fitbit_ids

        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, values, fields)


    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", test_ids="all", ouput_format="unwinded"):
        if test_ids == "all":
            test_ids = [t.test_id for p in self.participants for t in p.studies["MealTracker"]]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections_mealtracker["mealtracker"]
        return get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, ouput_format)

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", test_ids="all", sensors="all"):
        df_meals = []
        for x in self.participants:
            df_meals.append(x.mealtrackers_group.get_meals_results(timestamp_start, timestamp_end, "all", test_ids).astype("dataframe", True))
        df_meals = pd.concat(df_meals, axis=1)
        
        results = StudyResults([])
        for x in self.participants:
            results += x.mealtrackers_group.get_fitbit_results(timestamp_start, timestamp_end, sensors, fields)
        return results


    def get_fitbit_results_grouped(self, values, timestamp_start=None, timestamp_end=None, fitbit_ids="all",  bin_size=60, bin_unit="minute"):
        if fitbit_ids == "all":
            fitbit_ids = [y["sensor_id"] for p in self.participants for t in p.studies["MealTracker"] for key, value in t.sensors.items() for y in value if key == "fitbit"]
        else:
            if str(fitbit_ids).isnumeric():
                fitbit_ids = [int(fitbit_ids)]
            elif type(fitbit_ids) == list:
                fitbit_ids = fitbit_ids


        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results_grouped(fitbit_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)