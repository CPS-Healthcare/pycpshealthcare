from .participant_info import ParticipantInfo
from .results import StudyResults
import pandas as pd
from .mealtracker_functions import get_mealtracker_meals_results, get_mealtracker_fitbit_results,\
    get_mealtracker_fitbit_results_grouped

class MealTrackerStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="MealTracker").astype("Participant")

        
    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_ids="all", values="all", fields="all"):
        if specific_fitbit_ids == "all":
            fitbit_ids = [y["sensor_id"] for p in self.participants for t in p.studies["MealTracker"] for key, value in t.sensors.items() for y in value if key == "fitbit"]
        else:
            fitbit_ids = specific_fitbit_ids

        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, values, fields)


    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        if specific_test_ids == "all":
            test_ids = [t.test_id for p in self.participants for t in p.studies["MealTracker"]]
        else:
            fitbit_ids = specific_test_ids
        collection = self.connection.collections_mealtracker["mealtracker"]
        return get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format)

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", specific_fitbit_id="all", sensors="all"):
        df_meals = []
        for x in self.participants:
            df_meals.append(x.mealtrackers_group.get_meals_results(timestamp_start, timestamp_end, "all", specific_test_ids).astype("dataframe", True))
        df_meals = pd.concat(df_meals, axis=1)
        
        results = StudyResults([])
        for x in self.participants:
            results += x.mealtrackers_group.get_fitbit_results(timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
        return results


    def get_fitbit_results_grouped(self, values, timestamp_start=None, timestamp_end=None, specific_fitbit_ids="all",  bin_size=60, bin_unit="minute"):
        if specific_fitbit_ids == "all":
            fitbit_ids = [y["sensor_id"] for p in self.participants for t in p.studies["MealTracker"] for key, value in t.sensors.items() for y in value if key == "fitbit"]
        else:
            fitbit_ids = specific_fitbit_ids

        collection = self.connection.collections_mealtracker["realtimefitbit"]
        return get_mealtracker_fitbit_results_grouped(fitbit_ids, collection, timestamp_start, timestamp_end, specific_fitbit_ids, values, bin_size, bin_unit)