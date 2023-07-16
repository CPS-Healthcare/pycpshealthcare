from ..participant_info import ParticipantInfo
from ..results import StudyResults
import pandas as pd
from .values import realtime_fitbit_values
from .functions import get_mealtracker_meals_results, get_mealtracker_fitbit_results,\
    get_mealtracker_fitbit_results_grouped

class MealTrackerStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="MealTracker").astype("Participant")
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["MealTracker"]]

        
    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results(test_ids, collection, timestamp_start, timestamp_end, values)


    def get_meals_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", ouput_format="unwinded"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["MealTracker"]["MealTrack"]
        return get_mealtracker_meals_results(collection, test_ids, timestamp_start, timestamp_end, ouput_format)

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        df_meals = []
        df_meals.append(self.get_meals_results(timestamp_start, timestamp_end, test_ids, "unwinded").astype("dataframe", True))
        df_meals = pd.concat(df_meals, axis=1)
        
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(row["timestamp_start"], row["timestamp_end"], test_ids, values)
            results += temp
        return results


    def get_fitbit_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = realtime_fitbit_values 
        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    

    def get_fitbit_at_meals_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        df_meals = []
        df_meals.append(self.get_meals_results(timestamp_start, timestamp_end, test_ids).astype("dataframe", True))
        df_meals = pd.concat(df_meals, axis=1)
        print(df_meals)
        
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results_grouped(row["timestamp_start"], row["timestamp_end"], test_ids, values, bin_size, bin_unit)
            results += temp
        return results