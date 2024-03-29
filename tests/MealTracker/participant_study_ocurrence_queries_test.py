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
def test_fitbit(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="MealTracker").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                try:
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_meals(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="MealTracker").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                try:
                    next(
                        participant.studies["MealTracker"][0].get_meals_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["MealTracker"][0].get_meals_results(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit_at_meals(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="MealTracker").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                try:
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_at_meals(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_at_meals(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="MealTracker").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                try:
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_results_grouped(
                            timestamp_start=params["ts_start"],
                            timestamp_end=params["ts_end"],
                            bin_unit="day",
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_results_grouped(
                            timestamp_start=params["ts_start"],
                            timestamp_end=params["ts_end"],
                            bin_unit="day",
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit_at_meals_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="MealTracker").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                try:
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_at_meals_grouped(
                            timestamp_start=params["ts_start"],
                            timestamp_end=params["ts_end"],
                            bin_unit="day",
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["MealTracker"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["MealTracker"][0].get_fitbit_at_meals_grouped(
                            timestamp_start=params["ts_start"],
                            timestamp_end=params["ts_end"],
                            bin_unit="day",
                        )
                    )
