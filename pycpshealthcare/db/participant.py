from .Pancreas.participant_study import PancreasStudyOcurrence
from .Pancreas.participant_study import ParticipantPancreasStudiesGroup
from .MealTracker.participant_study import MealTrackerStudyOcurrence
from .MealTracker.participant_study import ParticipantMealTrackerStudiesGroup
from .SanPedro.participant_study import SanPedroStudyOcurrence
from .SanPedro.participant_study import ParticipantSanPedroStudiesGroup
from .Marcoleta.participant_study import ParticipantMarcoletaStudiesGroup
from .Marcoleta.participant_study import MarcoletaStudyOcurrence
from .ChronoNevado.participant_study import ChronoNevadoStudyOcurrence
from .ChronoNevado.participant_study import ParticipantChronoNevadoStudiesGroup
from .Chronotype.participant_study import ChronotypeStudyOcurrence
from .Chronotype.participant_study import ParticipantChronotypeStudiesGroup


class Participant:
    """
    A class for representing a GlobalInfo.ParticipantInfo MongoDB document
    as a Python object. Contains ParticipantStudiesGroup family instances for each
    of the studies.
    
    :param raw_data: A MongoDB document as a dictionary.
    :type raw_data:  dict

    :param connection: A pycpshealthcare.db.connector.CpsConnection instance.
    :type connection:  pycpshealthcare.db.connector.CpsConnection

    """
    def __init__(self, raw_data, connection):
        self.connection = connection
        self.id = raw_data["_id"] if "_id" in raw_data else ""
        self.name = raw_data["participant_name"] if "participant_name" in raw_data else ""
        self.studies_raw = raw_data["studies"] if "studies" in raw_data else ""
        self.studies = {}
        self.studies_groups = {}
        self.studies_groups["MealTracker"] = ParticipantMealTrackerStudiesGroup([], connection)
        self.studies_groups["Pancreas"] = ParticipantPancreasStudiesGroup([], connection)
        self.studies_groups["SanPedro"] = ParticipantSanPedroStudiesGroup([], connection)
        self.studies_groups["Marcoleta"] = ParticipantMarcoletaStudiesGroup([], connection)
        self.studies_groups["ChronoNevado"] = ParticipantChronoNevadoStudiesGroup([], connection)
        self._generate_studies_object()


    def _generate_studies_object(self):
        for study_type, study_raw in self.studies_raw.items():
            if study_type == "Pancreas":
                self.studies["Pancreas"] = []
                for study in study_raw:
                    study_obj = PancreasStudyOcurrence(study, self.connection)
                    self.studies["Pancreas"].append(study_obj)
                self.studies_groups["Pancreas"] = ParticipantPancreasStudiesGroup(self.studies["Pancreas"], self.connection)
            elif study_type == "MealTracker":
                self.studies["MealTracker"] = []
                for study in study_raw:
                    study_obj = MealTrackerStudyOcurrence(study, self.connection)
                    self.studies["MealTracker"].append(study_obj)
                self.studies_groups["MealTracker"] = ParticipantMealTrackerStudiesGroup(self.studies["MealTracker"], self.connection)
            elif study_type == "SanPedro":
                self.studies["SanPedro"] = []
                for study in study_raw:
                    study_obj = SanPedroStudyOcurrence(study, self.connection)
                    self.studies["SanPedro"].append(study_obj)
                self.studies_groups["SanPedro"] = ParticipantSanPedroStudiesGroup(self.studies["SanPedro"], self.connection)
            elif study_type == "Marcoleta":
                self.studies["Marcoleta"] = []
                for study in study_raw:
                    study_obj = MarcoletaStudyOcurrence(study, self.connection)
                    self.studies["Marcoleta"].append(study_obj)
                self.studies_groups["Marcoleta"] = ParticipantMarcoletaStudiesGroup(self.studies["Marcoleta"], self.connection)
            elif study_type == "ChronoNevado":
                self.studies["ChronoNevado"] = []
                for study in study_raw:
                    study_obj = ChronoNevadoStudyOcurrence(study, self.connection)
                    self.studies["ChronoNevado"].append(study_obj)
                self.studies_groups["ChronoNevado"] = ParticipantChronoNevadoStudiesGroup(self.studies["ChronoNevado"], self.connection)
            elif study_type == "Chronotype":
                self.studies["Chronotype"] = []
                for study in study_raw:
                    study_obj = ChronotypeStudyOcurrence(study, self.connection)
                    self.studies["Chronotype"].append(study_obj)
                self.studies_groups["Chronotype"] = ParticipantChronotypeStudiesGroup(self.studies["Chronotype"], self.connection)

    
    def __repr__(self) -> str:
        
        return f"{self.__class__} object (id: {self.id}, studies: {self.studies}"