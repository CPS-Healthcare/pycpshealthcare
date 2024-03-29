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
def test_cpet_raw_data(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_cpet_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_cpet_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


def test_cpet_participant_data():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_participant_data())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_test_data():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_test_data())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_environment_data():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_environment_data())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_participant_data():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_participant_data())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


@pytest.mark.parametrize("params, expected", date_params)
def test_finapres_rawdata(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_finapres_data(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_spo2_rawdata(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_spo2_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_spo2_raw_data(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_cpet_raw_data_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_cpet_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_cpet_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


def test_cpet_participant_data_grouped():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_participant_data_grouped())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_test_data_grouped():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_test_data_grouped())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_environment_data_grouped():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_environment_data_grouped())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


def test_cpet_participant_data_grouped():
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    for participant in participants:
        try:
            next(participant.studies["ChronoNevado"][0].get_cpet_participant_data_grouped())
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


@pytest.mark.parametrize("params, expected", date_params)
def test_finapres_rawdata(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_finapres_data_grouped(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_finapres_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )


@pytest.mark.parametrize("params, expected", date_params)
def test_spo2_rawdata(params, expected):
    connection = CpsConnection(
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
    )
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="ChronoNevado").astype("participant")
    if expected == True:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                try:
                    next(
                        participant.studies["ChronoNevado"][0].get_spo2_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
                    return
                except StopIteration:
                    pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            if len(participant.studies["ChronoNevado"]) > 0:
                with pytest.raises(StopIteration):
                    next(
                        participant.studies["ChronoNevado"][0].get_spo2_raw_data_grouped(
                            timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]
                        )
                    )
