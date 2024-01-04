from ..results import StudyResults
from ..participant_info import ParticipantInfo
from .functions import (
    get_marcoleta_sensor_results,
    get_marcoleta_sensor_results_grouped,
    get_marcoleta_metadata_results,
)
from .values import fitbit_v2_values, holter_values, autoreportes_values


class MarcoletaStudy:
    """
    A study class. Has methods for getting the data of all the sensors and measures of the respective study.\
    A study is defined as all the test ocurrences of a corresponding study type for all the participant.
    """

    def __init__(self, connection):
        self.connection = connection
        participant_info = ParticipantInfo(connection)
        self.participants = participant_info.get_participants(studies="Marcoleta").astype(
            "participant"
        )
        self.test_ids = [t.test_id for x in self.participants for t in x.studies["Marcoleta"]]

    def get_fitbit_v2_metadata_results(
        self, metadata_type, timestamp_start=None, timestamp_end=None, test_ids="all"
    ):
        if test_ids == "all":
            test_ids = self.test_ids
        else:
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Marcoleta"]["fitbit_v2_metadata"]
        return get_marcoleta_metadata_results(
            test_ids, collection, timestamp_start, timestamp_end, metadata_type
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
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results(
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
            if type(test_ids) == int:
                test_ids = [test_ids]
            elif type(test_ids) == list:
                test_ids = test_ids
        if values == "all":
            values = sensor_values
        collection = self.connection.collections["Marcoleta"][collection_name]
        return get_marcoleta_sensor_results_grouped(
            test_ids, collection, timestamp_start, timestamp_end, values, bin_size, bin_unit
        )

    return get_sensor_results_grouped


methods_parameters = {
    "get_fitbit_v2_results": _create_get_sensor_method(collection_name="fitbit_v2"),
    "get_holter_results": _create_get_sensor_method(collection_name="holter"),
    "get_autoreports_results": _create_get_sensor_method(collection_name="autoreports"),
}

grouped_methods_parameters = {
    "get_fitbit_v2_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitbit_v2", sensor_values=fitbit_v2_values
    ),
    "get_holter_results_grouped": _create_get_sensor_grouped_method(
        collection_name="holter", sensor_values=holter_values
    ),
    "get_autoreports_results_grouped": _create_get_sensor_grouped_method(
        collection_name="autoreports", sensor_values=autoreportes_values
    ),
}

for key, value in methods_parameters.items():
    setattr(MarcoletaStudy, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(MarcoletaStudy, key, value)
