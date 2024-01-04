import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pytest
from pymongo.errors import OperationFailure
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def test_connect():
    try:
        from pycpshealthcare.db.connectors import CpsConnection

        connection = CpsConnection(
            host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT
        )
        connection.client.server_info()
    except OperationFailure:
        pytest.fail("Failed to connect")


def test_study_import():
    try:
        from pycpshealthcare.db.Chronotype.study import ChronotypeStudy
    except ImportError:
        pytest.fail("Failed to import")


def test_study_ocurrence_import():
    try:
        from pycpshealthcare.db.Chronotype.participant_study import ChronotypeStudyOcurrence
    except ImportError:
        pytest.fail("Failed to import")


def test_participant_study_group_import():
    try:
        from pycpshealthcare.db.Chronotype.participant_study import (
            ParticipantChronotypeStudiesGroup,
        )
    except ImportError:
        pytest.fail("Failed to import")
