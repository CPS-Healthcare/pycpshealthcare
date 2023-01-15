from .participant_info import ParticipantInfo
from .results import StudyResults
import pandas as pd

class MealTrackerStudy:

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="MealTracker").astype("Participant")
        
    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, specific_fitbit_id="all", sensors="all", fields="all"):
        results = StudyResults([])
        for x in self.participants:
            results += x.mealtrackers_group.get_fitbit_results(timestamp_start, timestamp_end, specific_fitbit_id, sensors, fields)
        return results

    def get_meals_results(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", ouput_format="unwinded"):
        results = StudyResults([])
        for x in self.participants:
            results += x.mealtrackers_group.get_meals_results(self, timestamp_start, timestamp_end, fields, specific_test_ids, ouput_format)
        return results

    
    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, fields="all", specific_test_ids="all", specific_fitbit_id="all", sensors="all"):
        df_meals = []
        for x in self.participants:
            df_meals.append(x.mealtrackers_group.get_meals_results(timestamp_start, timestamp_end, "all", specific_test_ids).astype("dataframe", True))
        df_meals = pd.concat(df_meals, axis=1)
        
        results = StudyResults([])
        for x in self.participants:
            results += x.mealtrackers_group.get_fitbit_results(timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
        return results