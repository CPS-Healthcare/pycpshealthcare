from ..results import StudyResults
from .functions import (
    get_mealtracker_meals_results,
    get_mealtracker_fitbit_results,
    get_mealtracker_fitbit_results_grouped,
)
from .values import realtime_fitbit_values


class MealTrackerStudyOcurrence:

    """
    A study class. Has methods for getting the data of all the sensors and measures of the respective study.\
    A study is defined as all the test ocurrences of a corresponding study type for all the participant.
    """

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_id = study_info["test_id"]
        self.sensors = study_info["sensors"]
        self.start = study_info["timestamp_start"]
        self.end = study_info["timestamp_end"]

    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d") if self.end else "not finished"
        return f"{self.__class__} object (id: {self.test_id}, start_date:{init_date}, end_date:{end_date})"

    def get_fitbit_results(self, timestamp_start=None, timestamp_end=None, values="all"):
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
        :type values: str|list<str>|None, optional

        """
        test_ids = [self.test_id]
        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results(
            test_ids, collection, timestamp_start, timestamp_end, values
        )

    def get_meals_results(self, timestamp_start=None, timestamp_end=None, ouput_format="unwinded"):
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param ouput_format: unwinded|original
        :type ouput_format:  str

        """

        test_ids = [self.test_id]
        collection = self.connection.collections["MealTracker"]["MealTrack"]
        return get_mealtracker_meals_results(
            collection, test_ids, timestamp_start, timestamp_end, ouput_format
        )

    def get_fitbit_at_meals(self, timestamp_start=None, timestamp_end=None, values="all"):
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
        :type values: str|list<str>|None, optional

        """
        df_meals = self.get_meals_results(timestamp_start, timestamp_end).astype("dataframe", True)
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(row["timestamp_start"], row["timestamp_end"], values)
            results += temp
        return StudyResults(results)

    def get_fitbit_results_grouped(
        self, timestamp_start=None, timestamp_end=None, values="all", bin_size=60, bin_unit="minute"
    ):
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
        :type values: str|list<str>|None, optional

        :param bin_size: The width of the mobile window, defaults to 60.
        :type bin_size: int, optional

        :param bin_unit: The unit of the mobile window, defaults to minute. Options are minute, hour, day.
        :type bin_unit: str, optional
        """
        test_ids = [self.test_id]
        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results_grouped(
            test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit
        )

    def get_fitbit_at_meals_grouped(
        self, timestamp_start=None, timestamp_end=None, values="all", bin_size=60, bin_unit="minute"
    ):
        """
        :return: an iterable with the query results
        :rtype: pycpshealthcare.db.results.StudyResults

        :param timestamp_start: Datetime start filter for query. If not specified query will bring results from start of records.
        :type timestamp_start:  datetime.datetime|None, optional

        :param timestamp_end: Datetime start filter for query. If not specified query will bring results to end of records.
        :type timestamp_end:  datetime.datetime|None, optional

        :param values: The names (keys) of the values of the sensors to be returned by the query, defaults to "all" that brings
        :type values: str|list<str>|None, optional

        :param bin_size: The width of the mobile window, defaults to 60.
        :type bin_size: int, optional

        :param bin_unit: The unit of the mobile window, defaults to minute. Options are minute, hour, day.
        :type bin_unit: str, optional
        """
        test_ids = [self.test_id]
        df_meals = self.get_meals_results(timestamp_start, timestamp_end).astype("dataframe", True)
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results_grouped(
                row["timestamp_start"], row["timestamp_end"], test_ids, values, bin_size, bin_unit
            )
            results += temp
        return StudyResults(results)


class ParticipantMealTrackerStudiesGroup:
    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None

    def get_fitbit_results(
        self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"
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

        """
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = realtime_fitbit_values

        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results(
            test_ids, collection, timestamp_start, timestamp_end, values
        )

    def get_meals_results(
        self, timestamp_start=None, timestamp_end=None, test_ids="all", ouput_format="unwinded"
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

        :param ouput_format: unwinded|original
        :type ouput_format:  str

        """
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids

        collection = self.connection.collections["MealTracker"]["MealTrack"]
        return get_mealtracker_meals_results(
            collection, test_ids, timestamp_start, timestamp_end, ouput_format
        )

    def get_fitbit_at_meals(
        self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"
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

        """
        df_meals = self.get_meals_results(timestamp_start, timestamp_end, test_ids).astype(
            "dataframe", True
        )
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results(
                row["timestamp_start"], row["timestamp_end"], test_ids, values
            )
            results += temp
        return results

    def get_fitbit_results_grouped(
        self,
        timestamp_start=None,
        timestamp_end=None,
        test_ids="all",
        values="all",
        bin_size=60,
        bin_unit="minute",
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
        if test_ids == "all":
            test_ids = [x.test_id for x in self.data]
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["MealTracker"]["RealtimeFitbit"]
        return get_mealtracker_fitbit_results_grouped(
            test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit
        )

    def get_fitbit_at_meals_grouped(
        self,
        timestamp_start=None,
        timestamp_end=None,
        test_ids="all",
        values="all",
        bin_size=60,
        bin_unit="minute",
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
        df_meals = self.get_meals_results(timestamp_start, timestamp_end, test_ids).astype(
            "dataframe", True
        )
        results = StudyResults(iter([]))
        for index, row in df_meals.iterrows():
            temp = self.get_fitbit_results_grouped(
                row["timestamp_start"], row["timestamp_end"], test_ids, values, bin_size, bin_unit
            )
            results += temp
        return results
