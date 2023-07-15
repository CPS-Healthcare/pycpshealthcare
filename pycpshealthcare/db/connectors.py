"""
Submodule for managing MongoDB connection, dabases and connections.
"""

from pymongo import MongoClient
import pytz


class CpsConnection:
    """
    A class that manages the MongoDB client, databases and collections.

    :param connection_uri: The full MongoDB connection uri. Not needed if host, username and password are passed.
    :type connection_uri:  str, optional

    :param host: Database host. Not needed if connection_uri is passed.
    :type host:  str, optional

    :param username: Database username. Not needed if connection_uri is passed.
    :type username:  str, optional
    
    :param password: Database password. Not needed if connection_uri is passed.
    :type password:  str, optional
    
    :param port: Database port. Not needed if connection_uri is passed.
    :type port:  str|int, optional
    
    :param database_names: Database dict that maps pycpshealthcare studies names to databases names, defaults to {
        "mealtracker": "MealTracker",
        "pancreas": "Pancreas",
        "globalinfo": "GlobalInfo",
        "sanpedro": "SanPedro",
        "marcoleta": "Marcoleta",
        "chrononevado": "ChronoNevado"}
    :type database_names:  dict, optional

    :param tzinfo: Timezone for results, defaults to pytz.UTC.
    :type tzinfo:  pytz.Timezone, optional


    - Example with connection_uri::

        connection = CpsConnection(uri="mongodb://user:pass@localhost:27017")
        
    - Example without connection_uri::

        connection = CpsConnection(username="user", password="pass", host="localhost", port="27017")
    """

    def __init__(self, connection_uri=None, host=None,
                    username=None, password=None, port=None,
                    database_names = {
                        "mealtracker": "MealTracker",
                        "pancreas": "Pancreas",
                        "globalinfo": "GlobalInfo",
                        "sanpedro": "SanPedro",
                        "marcoleta": "Marcoleta",
                        "chrononevado": "ChronoNevado"
                        },
                    tzinfo=None):
        self.tzinfo = tzinfo if tzinfo else pytz.UTC
        if all([username, password, host]):
            uri = f"mongodb://{username}:{password}@{host}"
            if port: uri = f"{uri}:{port}"
            self.client = MongoClient(host=uri, tz_aware=True, tzinfo=self.tzinfo)
        elif connection_uri:
            self.client = MongoClient(host=connection_uri, tz_aware=True, tzinfo=self.tzinfo)
        else:
            raise Exception
        self.db_pancreas = self.client[database_names["pancreas"]]
        self.db_mealtracker = self.client[database_names["mealtracker"]]
        self.db_globalinfo = self.client[database_names["globalinfo"]]
        self.db_sanpedro = self.client[database_names["sanpedro"]]
        self.db_marcoleta = self.client[database_names["marcoleta"]]
        self.db_chrononevado = self.client[database_names["chrononevado"]]
        self.collections_pancreas = {
            "empatica": self.db_pancreas["empatica"],
            "equivital": self.db_pancreas["equivital"],
            "fitbit": self.db_pancreas["fitbit"],
            "fitnesspal_ejercicio": self.db_pancreas["fitnesspal_ejercicio"],
            "fitnesspal_nutricion": self.db_pancreas["fitnesspal_nutricion"],
            "guardian": self.db_pancreas["guardian"],
            "oscar": self.db_pancreas["oscar"],
        }
        self.collections_mealtracker = {
            "mealtracker": self.db_mealtracker["MealTrack"],
            "realtimefitbit": self.db_mealtracker["RealtimeFitbit"]
        }
        self.collections_globalinfo = {
            "participantinfo": self.db_globalinfo["ParticipantInfo"]
        }
        self.collections_sanpedro = {
            "holter": self.db_sanpedro["holter"],
            "fitbit": self.db_sanpedro["fitbit"],
            "fitbit_v2": self.db_sanpedro["fitbit_v2"],
            "fitbit_v2_metadata": self.db_sanpedro["fitbit_v2_metadata"],
            "inbody": self.db_sanpedro["inbody"],
            "alimentacion": self.db_sanpedro["alimentacion"],
            "patrones_minsal_2018": self.db_sanpedro["patrones_minsal_2018"],
            "freestyle_librelink": self.db_sanpedro["FreeStyle_LibreLink"],
        }
        self.collections_marcoleta = {
            "holter": self.db_marcoleta["holter"],
            "fitbit_v2": self.db_marcoleta["fitbit_v2"],
            "fitbit_v2_metadata": self.db_marcoleta["fitbit_v2_metadata"],
            "autoreports": self.db_marcoleta["autoreports"],
        }
        self.collections_chrononevado = {
            "CpetEnvironmentData": self.db_chrononevado["CpetEnvironmentData"],
            "CpetParticipantData": self.db_chrononevado["CpetParticipantData"],
            "CpetRawData": self.db_chrononevado["CpetRawData"],
            "CpetTestData": self.db_chrononevado["CpetTestData"],
            "FinapresData": self.db_chrononevado["FinapresData"],
            "Spo2RawData": self.db_chrononevado["Spo2RawData"],

        }
        
    def close(self):
        """
        Closes database connection.
        """
        self.client.close()

