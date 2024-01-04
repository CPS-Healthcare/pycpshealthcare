from ..results import StudyResults
from ..participant_info import ParticipantInfo
from .functions import (
    get_pancreas_sensor_results,
    get_pancreas_results_grouped,
    get_accel_vector_magnitude,
    get_accel_vector_magnitude_grouped,
)

from .values import (
    fitbit_values,
    empatica_values,
    equivital_values,
    guardian_values,
    fitnesspal_ejercicio_values,
    fitnesspal_nutricion_values,
    oscar_values,
)


class PancreasStudy:
    """
    A study class. Has methods for getting the data of all the sensors and measures of the respective study.\
    A study is defined as all the test ocurrences of a corresponding study type for all the participant.
    """

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Pancreas").astype(
            "participant"
        )
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["Pancreas"]]

    def get_empatica_accel_vector_magnitude(
        self, timestamp_start=None, timestamp_end=None, test_ids="all"
    ):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Pancreas"]["empatica"]
        return get_accel_vector_magnitude(test_ids, collection, timestamp_start, timestamp_end)

    def get_empatica_accel_vector_magnitude_grouped(
        self,
        timestamp_start=None,
        timestamp_end=None,
        test_ids="all",
        bin_size=60,
        bin_unit="minute",
    ):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Pancreas"]["empatica"]
        return get_accel_vector_magnitude_grouped(
            test_ids, collection, timestamp_start, timestamp_end, bin_size, bin_unit
        )


def _create_get_sensor_method(collection_name):
    def get_sensor_results(
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
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Pancreas"][collection_name]
        return get_pancreas_sensor_results(
            test_ids, collection, timestamp_start, timestamp_end, values
        )

    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(
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
            test_ids = self.test_ids
        else:
            if str(test_ids).isnumeric():
                test_ids = [int(test_ids)]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values
        collection = self.connection.collections["Pancreas"][collection_name]
        return get_pancreas_results_grouped(
            test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit
        )

    return get_sensor_results_grouped


methods_parameters = {
    "get_fitbit_results": _create_get_sensor_method(collection_name="fitbit"),
    "get_empatica_results": _create_get_sensor_method(collection_name="empatica"),
    "get_equivital_results": _create_get_sensor_method(collection_name="equivital"),
    "get_fitnesspal_ejercicio_results": _create_get_sensor_method(
        collection_name="fitnesspal_ejercicio"
    ),
    "get_fitnesspal_nutricion_results": _create_get_sensor_method(
        collection_name="fitnesspal_nutricion"
    ),
    "get_guardian_results": _create_get_sensor_method(collection_name="guardian"),
    "get_oscar_results": _create_get_sensor_method(collection_name="oscar"),
}

grouped_methods_parameters = {
    "get_fitbit_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitbit", sensor_values=fitbit_values
    ),
    "get_empatica_results_grouped": _create_get_sensor_grouped_method(
        collection_name="empatica", sensor_values=empatica_values
    ),
    "get_equivital_results_grouped": _create_get_sensor_grouped_method(
        collection_name="equivital", sensor_values=equivital_values
    ),
    "get_fitnesspal_ejercicio_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitnesspal_ejercicio", sensor_values=fitnesspal_ejercicio_values
    ),
    "get_fitnesspal_nutricion_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitnesspal_nutricion", sensor_values=fitnesspal_nutricion_values
    ),
    "get_guardian_results_grouped": _create_get_sensor_grouped_method(
        collection_name="guardian",
        sensor_values=guardian_values,
    ),
    "get_oscar_results_grouped": _create_get_sensor_grouped_method(
        collection_name="oscar", sensor_values=oscar_values
    ),
}

for key, value in methods_parameters.items():
    setattr(PancreasStudy, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(PancreasStudy, key, value)
