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
    ({"ts_start": datetime(2000,1, 1), "ts_end": datetime(2100, 1, 1)}, True),
    ({"ts_start": datetime(2100,1, 1), "ts_end": datetime(2000, 1, 1)}, False),
    ]


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_fitbit_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_fitbit_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit_v2(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_fitbit_v2_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_fitbit_v2_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    

def test_fitbit_v2_metadata():
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    for participant in participants:
        try:
            next(participant.studies_groups["SanPedro"].get_fitbit_v2_metadata_results(metadata_type="sleep"))
            return
        except StopIteration:
            pass
    assert False, "Iterator is empty"


@pytest.mark.parametrize("params, expected", date_params)
def test_holter(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_holter_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_holter_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    

@pytest.mark.parametrize("params, expected", date_params)
def test_alimentacion(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_alimentacion_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_alimentacion_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    

@pytest.mark.parametrize("params, expected", date_params)
def test_freestyle_librelink(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_freestyle_librelink_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_freestyle_librelink_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_inbody(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_inbody_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_inbody_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_patrones_minsal_2018(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_patrones_minsal_2018_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_patrones_minsal_2018_results(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_fitbit_v2_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_fitbit_v2_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_fitbit_v2_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    

@pytest.mark.parametrize("params, expected", date_params)
def test_holter_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_holter_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_holter_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    


@pytest.mark.parametrize("params, expected", date_params)
def test_alimentacion_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_alimentacion_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_alimentacion_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
    

@pytest.mark.parametrize("params, expected", date_params)
def test_freestyle_librelink_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_freestyle_librelink_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_freestyle_librelink_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_inbody_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_inbody_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_inbody_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))


@pytest.mark.parametrize("params, expected", date_params)
def test_patrones_minsal_2018_grouped(params, expected):
    
    connection = CpsConnection(host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT)
    participant_info = ParticipantInfo(connection)
    participants = participant_info.get_participants(studies="SanPedro").astype("participant")
    if expected == True:
        for participant in participants:
            try:
                next(participant.studies_groups["SanPedro"].get_patrones_minsal_2018_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))
                return
            except StopIteration:
                pass
        assert False, "Iterator is empty"
    else:
        for participant in participants:
            with pytest.raises(StopIteration):
                next(participant.studies_groups["SanPedro"].get_patrones_minsal_2018_results_grouped(timestamp_start=params["ts_start"], timestamp_end=params["ts_end"]))