import pandas as pd
from bson.codec_options import CodecOptions
from collections import defaultdict
from .studies.pancreas import ParticipantPancreasStudy
from .studies.pancreas import PancreasStudiesGroup
from .studies.mealtracker import ParticipantMealTrackerStudy
from .studies.mealtracker import MealTrackerStudiesGroup

class ParticipantInfo:

    def __init__(self, connection) -> None:
        self.connection = connection
        self.collection = connection.collections_globalinfo["participantinfo"]
        options = CodecOptions(tz_aware=True, tzinfo=connection.tzinfo)
        self.collection = self.collection.with_options(codec_options=options)

    def get_participants(self, participants_names=None, participants_ids=None):
        if participants_names:
            query = {
                "_id": {"$in": participants_ids}
            }
            results = self.collection.find(query)
        elif participants_names:
            query = {
                "participant_name": {"$in": participants_names}
            }
            results = self.collection.find(query)
        else:
            results = self.collection.find()
        return ParticipantsResults(results, self.connection)



class Participant:
    def __init__(self, raw_data, connection):
        self.connection = connection
        self.id = raw_data["_id"] if "_id" in raw_data else ""
        self.name = raw_data["participant_name"] if "participant_name" in raw_data else ""
        self.studies_raw = raw_data["studies"] if "studies" in raw_data else ""
        self.studies = {}
        self.mealtrackers_group = MealTrackerStudiesGroup([], connection)
        self.pancreas_group = PancreasStudiesGroup([], connection)
        self.generate_studies_object()


    def generate_studies_object(self):
        for study_type, study_raw in self.studies_raw.items():
            if study_type == "Pancreas":
                self.studies["Pancreas"] = []
                for study in study_raw:
                    study_obj = ParticipantPancreasStudy(study, self.connection)
                    self.studies["Pancreas"].append(study_obj)
                self.pancreas_group = PancreasStudiesGroup(self.studies["Pancreas"], self.connection)
            elif study_type == "MealTracker":
                self.studies["MealTracker"] = []
                for study in study_raw:
                    study_obj = ParticipantMealTrackerStudy(study, self.connection)
                    self.studies["MealTracker"].append(study_obj)
                self.mealtrackers_group = MealTrackerStudiesGroup(self.studies["MealTracker"], self.connection)



class ParticipantsResults:
    def __init__(self, results, connection):
        self.results = results
        self.connection = connection

    def __iter__(self):
        return ParticipantIterable(self)

    def astype(self, out_type):
        if out_type == list or out_type == "list":
            return list(self.results)
        elif out_type == pd.DataFrame or out_type == "dataframe":
            return pd.DataFrame(self.results)
        elif out_type == "class":
            return list(map(lambda x: Participant(x, self.connection), self.results))


class ParticipantIterable:

    def __init__(self, element):
        self.iterable = element
        self._index = 0


    def __next__(self):
        self._index += 1
        return next(self.iterable.results)
