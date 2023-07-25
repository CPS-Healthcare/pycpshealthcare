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

        """
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
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param test_ids: The ids of the tests to be queried, defaults to "all" that brings data of all the test ids.
        :type test_ids: int|list<int>|None, optional

        :param ouput_format: unwinded|original
        :type ouput_format:  str

        """
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

        """
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