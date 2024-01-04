import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pytest
from pymongo.errors import OperationFailure
from pycpshealthcare.db.connectors import CpsConnection
from pycpshealthcare.db.participant_info import ParticipantInfo
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

date_params = [
    ({"ts_start": datetime(2000, 1, 1), "ts_end": datetime(2100, 1, 1)}, True),
    ({"ts_start": datetime(2100, 1, 1), "ts_end": datetime(2000, 1, 1)}, False),
]


@pytest.mark.parametrize("params, expected", date_params)
def test_activitymodule(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_activitymodule_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_activitymodule_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_corepill(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_corepill_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_corepill_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_equivital(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_equivital_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_equivital_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_oscar(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_oscar_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_oscar_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_salivette(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_salivette_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_salivette_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_survey_data(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_survey_data_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_survey_data_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_activitymodule_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_activitymodule_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_activitymodule_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_corepill_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_corepill_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_corepill_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_equivital_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_equivital_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_equivital_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_oscar_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_oscar_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_oscar_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_salivette_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="Chronotype").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                try:
                    next(
                        participant.studies["Chronotype"][0].get_salivette_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["Chronotype"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["Chronotype"][0].get_salivette_results_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
