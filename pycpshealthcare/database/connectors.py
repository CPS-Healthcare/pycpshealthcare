from pymongo import MongoClient
import pytz


class CpsConnection:

    def __init__(self, connection_uri=None, host=None,
                    username=None, password=None, port=None,
                    database_names = {
                        "mealtracker": "MealTracker",
                        "pancreas": "Pancreas",
                        "globalinfo": "GlobalInfo",
                        "sanpedro": "SanPedro"
                        },
                    tzinfo=None):
        self.tzinfo = tzinfo if tzinfo else pytz.UTC
        if all([username, password, host]):
            uri = f"mongodb://{username}:{password}@{host}"
            if port: uri = f"{uri}:{port}"
            self.client = MongoClient(host=uri, tz_aware=True)
        elif connection_uri:
            self.client = MongoClient(host=connection_uri, tz_aware=True)
        else:
            raise Exception
        self.db_pancreas = self.client[database_names["pancreas"]]
        self.db_mealtracker = self.client[database_names["mealtracker"]]
        self.db_globalinfo = self.client[database_names["globalinfo"]]
        self.db_sanpedro = self.client[database_names["sanpedro"]]
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
        
    def close(self):
        self.client.close()

