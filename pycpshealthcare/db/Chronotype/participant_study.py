from .functions import get_chronotype_sensor_results, get_chronotype_results_grouped
from .values import activitymodule_values, corepill_values, equivital_values,\
    oscar_values, salivette_values, sunsprite_values

# TODO: Test this classes!


class ChronotypeStudyOcurrence:

    """
    A study ocurrence class. Has methods for getting the data of all the sensors and measures of the respective study.\
    An ocurrence is defined as a unit test and is related to only one participant.
    """

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_name = study_info["test_id"]
        self.test_id = study_info["test_id"]
        self.start = study_info["timestamp_start"]
        self.end = study_info["timestamp_end"] 
        self.study_info = study_info

    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.test_id}, start_date:{init_date}, end_date:{end_date})"


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, values="all"):
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
        collection = self.connection.collections["Chronotype"][collection_name]
        return get_chronotype_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, values="all", bin_size=60, bin_unit="minute"):
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
        if values == "all":
            values = sensor_values
        collection = self.connection.collections["Chronotype"][collection_name]
        return get_chronotype_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    

methods_parameters = {
    "get_activitymodule_results": _create_get_sensor_method(collection_name="activitymodule"),
    "get_corepill_results": _create_get_sensor_method(collection_name="corepill"),
    "get_equivital_results": _create_get_sensor_method(collection_name="equivital"),
    "get_oscar_results": _create_get_sensor_method(collection_name="oscar"),
    "get_salivette_results": _create_get_sensor_method(collection_name="salivette"),
    "get_sunsprite_results": _create_get_sensor_method(collection_name="sunsprite"),
    "get_survey_data_results": _create_get_sensor_method(collection_name="survey_data"),
}

grouped_methods_parameters = {
    "get_activitymodule_results_grouped": _create_get_sensor_grouped_method(
        collection_name="activitymodule",
        sensor_values=activitymodule_values
        ),
    "get_corepill_results_grouped": _create_get_sensor_grouped_method(
        collection_name="corepill",
        sensor_values=corepill_values
        ),
    "get_equivital_results_grouped": _create_get_sensor_grouped_method(
        collection_name="equivital",
        sensor_values=equivital_values
        ),
    "get_oscar_results_grouped": _create_get_sensor_grouped_method(
        collection_name="oscar",
        sensor_values=oscar_values
        ),
    "get_salivette_results_grouped": _create_get_sensor_grouped_method(
        collection_name="salivette",
        sensor_values=salivette_values
        ),
    "get_sunsprite_results_grouped": _create_get_sensor_grouped_method(
        collection_name="sunsprite",
        sensor_values=sunsprite_values
        ),
}

for key, value in methods_parameters.items():
    setattr(ChronotypeStudyOcurrence, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(ChronotypeStudyOcurrence, key, value)



class ParticipantChronotypeStudiesGroup:
    """
    A participant studies group class. Has methods for getting the data of all the sensors and measures of the respective studies group.\
    A participant studies group is defined as all the ocurrences of a corresponding study type for a specific participant and is related to only one participant.
    """

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all"):
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

        collection = self.connection.collections["Chronotype"][collection_name]
        return get_chronotype_sensor_results(test_ids, collection, timestamp_start, timestamp_end, values)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, test_ids="all", values="all", bin_size=60, bin_unit="minute"):
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

        if values == "all":
            values = sensor_values
        collection = self.connection.collections["Chronotype"][collection_name]
        return get_chronotype_results_grouped(test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit)
    return get_sensor_results_grouped

methods_parameters_2 = {
    "get_activitymodule_results": _create_get_sensor_method_2(collection_name="activitymodule"),
    "get_corepill_results": _create_get_sensor_method_2(collection_name="corepill"),
    "get_equivital_results": _create_get_sensor_method_2(collection_name="equivital"),
    "get_oscar_results": _create_get_sensor_method_2(collection_name="oscar"),
    "get_salivette_results": _create_get_sensor_method_2(collection_name="salivette"),
    "get_sunsprite_results": _create_get_sensor_method_2(collection_name="sunsprite"),
    "get_survey_data_results": _create_get_sensor_method_2(collection_name="survey_data"),
}

grouped_methods_parameters_2 = {
    "get_activitymodule_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="activitymodule",
        sensor_values=activitymodule_values
        ),
    "get_corepill_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="corepill",
        sensor_values=corepill_values
        ),
    "get_equivital_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="equivital",
        sensor_values=equivital_values
        ),
    "get_oscar_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="oscar",
        sensor_values=oscar_values
        ),
    "get_salivette_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="salivette",
        sensor_values=salivette_values
        ),
    "get_sunsprite_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="sunsprite",
        sensor_values=sunsprite_values
        ),
}

for key, value in methods_parameters_2.items():
    setattr(ParticipantChronotypeStudiesGroup, key, value)

for key, value in grouped_methods_parameters_2.items():
    setattr(ParticipantChronotypeStudiesGroup, key, value)