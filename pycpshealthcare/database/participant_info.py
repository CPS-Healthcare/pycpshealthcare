import pandas as pd
from bson.codec_options import CodecOptions
from itertools import chain
from .participant import Participant

class ParticipantInfo:

    def __init__(self, connection) -> None:
        self.connection = connection
        self.collection = connection.collections_globalinfo["participantinfo"]
        options = CodecOptions(tz_aware=True, tzinfo=connection.tzinfo)
        self.collection = self.collection.with_options(codec_options=options)

    def get_participants(self, participants_names=None, participants_ids=None, studies='all'):
        if participants_names:
            query = {
                "_id": {"$in": participants_names}
            }
            results = self.collection.find(query)
        elif participants_ids:
            query = {
                "participant_name": {"$in": participants_ids}
            }
        else:
            query = {}

        if studies != "all":
            study_filter = {"$or": []}
            if type(studies) == str:
                studies = [studies]
            for study in studies:
                if study.lower() == "pancreas":
                    study_filter["$or"].append({f"studies.Pancreas": {"$exists": True}})
                elif study.lower() == "mealtracker":
                    study_filter["$or"].append({f"studies.MealTracker": {"$exists": True}})
                elif study.lower() == "sanpedro":
                    study_filter["$or"].append({f"studies.SanPedro": {"$exists": True}})
            query.update(study_filter)
        parameters = {"filter": query} if query else {}
        results = self.collection.find(**parameters)
        return ParticipantsResults(results, self.connection)


class ParticipantsResults:
    def __init__(self, results, connection):
        self.results = results
        self.connection = connection

    def __iter__(self):
        return ParticipantIterable(self)

    def __add__(self, other):
        return ParticipantsResults(chain(self.results, other.results))


    def astype(self, out_type):
        if out_type == list or out_type == "list":
            return list(self.results)
        elif out_type == pd.DataFrame or out_type == "dataframe":
            return pd.DataFrame(self.results)
        elif out_type.lower() == "participant":
            return list(map(lambda x: Participant(x, self.connection), self.results))
        else:
            raise TypeError


class ParticipantIterable:

    def __init__(self, element):
        self.iterable = element
        self._index = 0


    def __next__(self):
        self._index += 1
        return next(self.iterable.results)