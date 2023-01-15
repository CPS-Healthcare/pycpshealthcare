from .pancreas_utils import ParticipantPancreasStudy
from .pancreas_utils import PancreasStudiesGroup
from .mealtracker_utils import ParticipantMealTrackerStudy
from .mealtracker_utils import MealTrackerStudiesGroup



class Participant:
    def __init__(self, raw_data, connection):
        self.connection = connection
        self.id = raw_data["_id"] if "_id" in raw_data else ""
        self.name = raw_data["participant_name"] if "participant_name" in raw_data else ""
        self.studies_raw = raw_data["studies"] if "studies" in raw_data else ""
        self.studies = {}
        self.mealtrackers_group = MealTrackerStudiesGroup([], connection)
        self.pancreas_group = PancreasStudiesGroup([], connection)
        self._generate_studies_object()


    def _generate_studies_object(self):
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

