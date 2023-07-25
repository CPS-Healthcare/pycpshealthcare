import pandas as pd
from bson.codec_options import CodecOptions
from itertools import chain
from .participant import Participant

class ParticipantInfo:

    def __init__(self, connection) -> None:
        self.connection = connection
        self.collection = connection.collections["GlobalInfo"]["ParticipantInfo"]
        options = CodecOptions(tz_aware=True, tzinfo=connection.tzinfo)
        self.collection = self.collection.with_options(codec_options=options)

    def get_participants(self, participants_names=None, participants_ids=None, studies='all', bring_id=False):
        if participants_names:
            query = {
                "_id": {"$in": participants_ids}
            }
            results = self.collection.find(query)
        elif participants_ids:
            query = {
                "participant_name": {"$in": participants_names}
            }
        else:
            query = {}

        if (type(studies) == str and studies != "all") or (type(studies) == list and "all" not in studies):
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
                elif study.lower() == "marcoleta":
                    study_filter["$or"].append({f"studies.Marcoleta": {"$exists": True}})
                elif study.lower() == "chrononevado":
                    study_filter["$or"].append({f"studies.ChronoNevado": {"$exists": True}})
                elif study.lower() == "chronotype":
                    study_filter["$or"].append({f"studies.Chronotype": {"$exists": True}})
            query.update(study_filter)
        parameters = {"filter": query} if query else {}
        if bring_id==False:
            parameters["projection"] = {"_id": 0}
        results = self.collection.find(**parameters)
        return ParticipantsResults(results, self.connection)


class ParticipantsResults:
    def __init__(self, results, connection):
        self.results = results
        self.connection = connection
        self._index = 0

    def __iter__(self):
        return self
  
    def __next__(self):
        item = next(self.results, None)
        if item is None:
            raise StopIteration
        else:
            self._index += 1
        return item

    def __add__(self, other):
        return ParticipantsResults(chain(self.results, other.results), self.connection)


    def astype(self, out_type, split_columns=False):
        if out_type == list or out_type == "list":
            return list(self.results)
        elif out_type == pd.DataFrame or out_type == "dataframe":
            if split_columns:
                df = pd.json_normalize(self.results)
                return df
            return pd.DataFrame(self.results)
        elif out_type.lower() == "participant":
            return list(map(lambda x: Participant(x, self.connection), self.results))
        else:
            raise TypeError

