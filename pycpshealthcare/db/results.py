import pandas as pd
from itertools import chain


class StudyResults:
    def __init__(self, results):
        self.results = results
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
        return StudyResults(chain(self.results, other.results))

    def astype(self, out_type, split_columns=False):
        if out_type == list or out_type == "list":
            return list(self.results)
        elif out_type == pd.DataFrame or out_type == "dataframe":
            if split_columns:
                df = pd.DataFrame(self.results)
                if "values" in df.columns:
                    df = pd.concat(
                        [df.drop(["values"], axis=1), df["values"].apply(pd.Series)], axis=1
                    )
                return df
            return pd.DataFrame(self.results)
