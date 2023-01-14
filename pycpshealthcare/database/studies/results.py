import pandas as pd
from itertools import chain

class StudyResults:
    def __init__(self, results):
        self.results = results

    def __iter__(self):
        return StudyIterable(self)

    def __add__(self, other):
        return StudyResults(chain(self.results, other.results))

    def astype(self, out_type, split_columns=False):
        if out_type == list or out_type == "list":
            return list(self.results)
        elif out_type == pd.DataFrame or out_type == "dataframe":
            if split_columns:
                df = pd.DataFrame(self.results)
                if "values" in df.columns:
                    df = pd.concat([df.drop(["values"], axis=1), df["values"].apply(pd.Series)], axis=1)
                elif "records" in df.columns:
                    df = pd.concat([df.drop(["records"], axis=1), df["records"].apply(pd.Series)], axis=1)
                return df
            return pd.DataFrame(self.results)


class StudyIterable:

    def __init__(self, element):
        self.iterable = element
        self._index = 0


    def __next__(self):
        self._index += 1
        return next(self.iterable.results)