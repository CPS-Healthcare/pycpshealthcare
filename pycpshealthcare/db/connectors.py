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
                        "MealTracker": "MealTrackerV2",
                        "Pancreas": "Pancreas",
                        "GlobalInfo": "GlobalInfo",
                        "SanPedro": "SanPedro",
                        "Marcoleta": "Marcoleta",
                        "ChronoNevado": "ChronoNevado",
                        "Chronotype": "Chronotype",
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
        self.dbs = {
            "GlobalInfo": self.client[database_names["GlobalInfo"]],
            "Pancreas": self.client[database_names["Pancreas"]],
            "MealTracker": self.client[database_names["MealTracker"]],
            "SanPedro": self.client[database_names["SanPedro"]],
            "Marcoleta": self.client[database_names["Marcoleta"]],
            "ChronoNevado": self.client[database_names["ChronoNevado"]],
            "Chronotype": self.client[database_names["Chronotype"]],
        }
        self.collections = {}
        self.collections["Pancreas"] = {
            "empatica": self.dbs["Pancreas"]["empatica"],
            "equivital": self.dbs["Pancreas"]["equivital"],
            "fitbit": self.dbs["Pancreas"]["fitbit"],
            "fitnesspal_ejercicio": self.dbs["Pancreas"]["fitnesspal_ejercicio"],
            "fitnesspal_nutricion": self.dbs["Pancreas"]["fitnesspal_nutricion"],
            "guardian": self.dbs["Pancreas"]["guardian"],
            "oscar": self.dbs["Pancreas"]["oscar"],
        }
        self.collections["MealTracker"] = {
            "MealTrack": self.dbs["MealTracker"]["MealTrack"],
            "RealtimeFitbit": self.dbs["MealTracker"]["RealtimeFitbit"]
        }
        self.collections["GlobalInfo"] = {
            "ParticipantInfo": self.dbs["GlobalInfo"]["ParticipantInfo"]
        }
        self.collections["SanPedro"] = {
            "holter": self.dbs["SanPedro"]["holter"],
            "fitbit": self.dbs["SanPedro"]["fitbit"],
            "fitbit_v2": self.dbs["SanPedro"]["fitbit_v2"],
            "fitbit_v2_metadata": self.dbs["SanPedro"]["fitbit_v2_metadata"],
            "inbody": self.dbs["SanPedro"]["inbody"],
            "alimentacion": self.dbs["SanPedro"]["alimentacion"],
            "patrones_minsal_2018": self.dbs["SanPedro"]["patrones_minsal_2018"],
            "freestyle_librelink": self.dbs["SanPedro"]["FreeStyle_LibreLink"],
        }
        self.collections["Marcoleta"] = {
            "holter": self.dbs["Marcoleta"]["holter"],
            "fitbit_v2": self.dbs["Marcoleta"]["fitbit_v2"],
            "fitbit_v2_metadata": self.dbs["Marcoleta"]["fitbit_v2_metadata"],
            "autoreports": self.dbs["Marcoleta"]["autoreports"],
        }
        self.collections["ChronoNevado"] = {
            "CpetEnvironmentData": self.dbs["ChronoNevado"]["CpetEnvironmentData"],
            "CpetParticipantData": self.dbs["ChronoNevado"]["CpetParticipantData"],
            "CpetRawData": self.dbs["ChronoNevado"]["CpetRawData"],
            "CpetTestData": self.dbs["ChronoNevado"]["CpetTestData"],
            "FinapresData": self.dbs["ChronoNevado"]["FinapresData"],
            "FinapresRawData": self.dbs["ChronoNevado"]["FinapresRawData"],
            "Spo2RawData": self.dbs["ChronoNevado"]["Spo2RawData"],

        }
        self.collections["Chronotype"] = {
            "activitymodule": self.dbs["Chronotype"]["activitymodule"],
            "corepill": self.dbs["Chronotype"]["corepill"],
            "equivital": self.dbs["Chronotype"]["equivital"],
            "oscar": self.dbs["Chronotype"]["oscar"],
            "salivette": self.dbs["Chronotype"]["salivette"],
            "sunsprite": self.dbs["Chronotype"]["sunsprite"],
            "survey_data": self.dbs["Chronotype"]["survey_data"],
        }
        
    def close(self):
        """
        Closes database connection.
        """
        self.client.close()

