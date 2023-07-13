from .functions import get_pancreas_sensor_results, get_pancreas_results_grouped,\
    get_accel_vector_magnitude, get_accel_vector_magnitude_grouped
from .values import fitbit_values, empatica_values, equivital_values, guardian_values, \
    fitnesspal_ejercicio_values, fitnesspal_nutricion_values, oscar_values

# TODO: Test this classes!


class ParticipantPancreasStudy:

    def __init__(self, study_info, connection):
        self.connection = connection
        self.test_name = study_info["Nombre prueba"]
        self.test_id = study_info["test_id"]
        self.start = study_info["Desde"]
        self.end = study_info["Hasta"] 
        self.study_info = study_info

    def __repr__(self) -> str:
        init_date = self.start.strftime("%Y-%m-%d")
        end_date = self.end.strftime("%Y-%m-%d")
        return f"{self.__class__} object (id:{self.test_id}, start_date:{init_date}, end_date:{end_date})"

    def get_empatica_accel_vector_magnitude(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["empatica"]
        return get_accel_vector_magnitude(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids)
    
    def get_empatica_accel_vector_magnitude(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas["empatica"]
        return get_accel_vector_magnitude_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, bin_size, bin_unit)
    


def _create_get_sensor_method(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_id="all", sensors="all", fields="all"):
        test_ids = [self.test_id]
        collection = self.connection.collections_pancreas[collection_name]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_id, sensors, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        test_ids = [self.test_id]
        if values == "all":
            values = sensor_values
        collection = self.connection.collections_pancreas[collection_name]
        return get_pancreas_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped
    

methods_parameters = {
    "get_fitbit_results": _create_get_sensor_method(collection_name="fitbit"),
    "get_empatica_results": _create_get_sensor_method(collection_name="empatica"),
    "get_equivital_results": _create_get_sensor_method(collection_name="equivital"),
    "get_fitnesspal_ejercicio_results": _create_get_sensor_method(collection_name="fitnesspal_ejercicio"),
    "get_fitnesspal_nutricion_results": _create_get_sensor_method(collection_name="fitnesspal_nutricion"),
    "get_guardian_results": _create_get_sensor_method(collection_name="guardian"),
    "get_oscar_results": _create_get_sensor_method(collection_name="oscar"),
}

grouped_methods_parameters = {
    "get_fitbit_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitbit",
        sensor_values=fitbit_values
        ),
    "get_empatica_results_grouped": _create_get_sensor_grouped_method(
        collection_name="empatica",
        sensor_values=empatica_values
        ),
    "get_equivital_results_grouped": _create_get_sensor_grouped_method(
        collection_name="equivital",
        sensor_values=equivital_values
        ),
    "get_fitnesspal_ejercicio_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitnesspal_ejercicio",
        sensor_values=fitnesspal_ejercicio_values
        ),
    "get_fitnesspal_nutricion_results_grouped": _create_get_sensor_grouped_method(
        collection_name="fitnesspal_nutricion",
        sensor_values=fitnesspal_nutricion_values
        ),
    "get_guardian_results_grouped": _create_get_sensor_grouped_method(
        collection_name="guardian",
        sensor_values=guardian_values,
        ),
    "get_oscar_results_grouped": _create_get_sensor_grouped_method(
        collection_name="oscar",
        sensor_values=oscar_values),
}

for key, value in methods_parameters.items():
    setattr(ParticipantPancreasStudy, key, value)

for key, value in grouped_methods_parameters.items():
    setattr(ParticipantPancreasStudy, key, value)



class ParticipantPancreasStudiesGroup:

    def __init__(self, data, connection):
        self.connection = connection
        self.data = data

    def get_test_instance(self, specific_test_id):
        for study in self.data:
            if study.test_id == specific_test_id:
                return study
        return None


def _create_get_sensor_method_2(collection_name):
    def get_sensor_results(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", sensors="all", fields="all"):
        test_ids = [x.test_id for x in self.data]
        collection = self.connection.collections_pancreas[collection_name]
        return get_pancreas_sensor_results(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, sensors, fields)
    return get_sensor_results


def _create_get_sensor_grouped_method_2(collection_name, sensor_values):
    def get_sensor_results_grouped(self, timestamp_start=None, timestamp_end=None, specific_test_ids="all", values="all", bin_size=60, bin_unit="minute"):
        test_ids = [x.test_id for x in self.data]
        if values == "all":
            values = sensor_values
        collection = self.connection.collections_pancreas[collection_name]
        return get_pancreas_results_grouped(test_ids, collection, timestamp_start, timestamp_end, specific_test_ids, values, bin_size, bin_unit)
    return get_sensor_results_grouped

methods_parameters_2 = {
    "get_fitbit_results": _create_get_sensor_method_2(collection_name="fitbit"),
    "get_empatica_results": _create_get_sensor_method_2(collection_name="empatica"),
    "get_equivital_results": _create_get_sensor_method_2(collection_name="equivital"),
    "get_fitnesspal_ejercicio_results": _create_get_sensor_method_2(collection_name="fitnesspal_ejercicio"),
    "get_fitnesspal_nutricion_results": _create_get_sensor_method_2(collection_name="fitnesspal_nutricion"),
    "get_guardian_results": _create_get_sensor_method_2(collection_name="guardian"),
    "get_oscar_results": _create_get_sensor_method_2(collection_name="oscar"),
}

grouped_methods_parameters_2 = {
    "get_fitbit_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="fitbit",
        sensor_values=fitbit_values
        ),
    "get_empatica_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="empatica",
        sensor_values=empatica_values
        ),
    "get_equivital_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="equivital",
        sensor_values=equivital_values
        ),
    "get_fitnesspal_ejercicio_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="fitnesspal_ejercicio",
        sensor_values=fitnesspal_ejercicio_values
        ),
    "get_fitnesspal_nutricion_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="fitnesspal_nutricion",
        sensor_values=fitnesspal_nutricion_values
        ),
    "get_guardian_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="guardian",
        sensor_values=guardian_values,
        ),
    "get_oscar_results_grouped": _create_get_sensor_grouped_method_2(
        collection_name="oscar",
        sensor_values=oscar_values),
}

for key, value in methods_parameters_2.items():
    setattr(ParticipantPancreasStudiesGroup, key, value)

for key, value in grouped_methods_parameters_2.items():
    setattr(ParticipantPancreasStudiesGroup, key, value)