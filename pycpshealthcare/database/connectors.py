from pymongo import MongoClient
import pytz


class CpsConnection:

    def __init__(self, connection_uri=None, host=None,
                    username=None, password=None, port=None, tzinfo=None):
        self.tzinfo = tzinfo if tzinfo else pytz.UTC
        if all([username, password, host]):
            uri = f"mongodb://{username}:{password}@{host}"
            if port: uri = f"{uri}:{port}"
            self.client = MongoClient(host=uri)
        elif connection_uri:
            self.client = MongoClient(host=connection_uri)
        else:
            raise Exception
        self.db_pancreas = self.client["Pancreas"]
        self.db_mealtracker = self.client["AlphaDB"]
        self.db_globalinfo = self.client["GlobalInfo"]
        self.collections_pancreas = {
            "empatica": self.db_pancreas["empatica"],
            "equitival": self.db_pancreas["equitival"],
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
        
    def close(self):
        self.client.close()

