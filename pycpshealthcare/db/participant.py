from .Pancreas.participant_study import ParticipantPancreasStudy
from .Pancreas.participant_study import ParticipantPancreasStudiesGroup
from .MealTracker.participant_study import ParticipantMealTrackerStudy
from .MealTracker.participant_study import ParticipantMealTrackerStudiesGroup
from .SanPedro.participant_study import ParticipantSanPedroStudy
from .SanPedro.participant_study import ParticipantSanPedroStudiesGroup
from .Marcoleta.participant_study import ParticipantMarcoletaStudiesGroup
from .Marcoleta.participant_study import ParticipantMarcoletaStudy
from .ChronoNevado.participant_study import ParticipantChronoNevadoStudy
from .ChronoNevado.participant_study import ParticipantChronoNevadoStudiesGroup


class Participant:
    def __init__(self, raw_data, connection):
        self.connection = connection
        self.id = raw_data["_id"] if "_id" in raw_data else ""
        self.name = raw_data["participant_name"] if "participant_name" in raw_data else ""
        self.studies_raw = raw_data["studies"] if "studies" in raw_data else ""
        self.studies = {}
        self.mealtrackers_group = ParticipantMealTrackerStudiesGroup([], connection)
        self.pancreas_group = ParticipantPancreasStudiesGroup([], connection)
        self.sanpedro_group = ParticipantSanPedroStudiesGroup([], connection)
        self.marcoleta_group = ParticipantMarcoletaStudiesGroup([], connection)
        self.chrononevado_group = ParticipantChronoNevadoStudiesGroup([], connection)
        self._generate_studies_object()


    def _generate_studies_object(self):
        for study_type, study_raw in self.studies_raw.items():
            if study_type == "Pancreas":
                self.studies["Pancreas"] = []
                for study in study_raw:
                    study_obj = ParticipantPancreasStudy(study, self.connection)
                    self.studies["Pancreas"].append(study_obj)
                self.pancreas_group = ParticipantPancreasStudiesGroup(self.studies["Pancreas"], self.connection)
            elif study_type == "MealTracker":
                self.studies["MealTracker"] = []
                for study in study_raw:
                    study_obj = ParticipantMealTrackerStudy(study, self.connection)
                    self.studies["MealTracker"].append(study_obj)
                self.mealtrackers_group = ParticipantMealTrackerStudiesGroup(self.studies["MealTracker"], self.connection)
            elif study_type == "SanPedro":
                self.studies["SanPedro"] = []
                for study in study_raw:
                    study_obj = ParticipantSanPedroStudy(study, self.connection)
                    self.studies["SanPedro"].append(study_obj)
                self.sanpedro_group = ParticipantSanPedroStudiesGroup(self.studies["SanPedro"], self.connection)
            elif study_type == "Marcoleta":
                self.studies["Marcoleta"] = []
                for study in study_raw:
                    study_obj = ParticipantMarcoletaStudy(study, self.connection)
                    self.studies["Marcoleta"].append(study_obj)
                self.marcoleta_group = ParticipantMarcoletaStudiesGroup(self.studies["Marcoleta"], self.connection)
            elif study_type == "ChronoNevado":
                self.studies["ChronoNevado"] = []
                for study in study_raw:
                    study_obj = ParticipantChronoNevadoStudy(study, self.connection)
                    self.studies["ChronoNevado"].append(study_obj)
                self.marcoleta_group = ParticipantChronoNevadoStudiesGroup(self.studies["ChronoNevado"], self.connection)

    
    def __repr__(self) -> str:
        
        return f"{self.__class__} object (id: {self.id}, studies: {self.studies}"