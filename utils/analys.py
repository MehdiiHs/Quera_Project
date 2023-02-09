import pandas as df
import numpy as np

def list_to_numpy_array(lst):
    if isinstance(lst, list):
        items = [list_to_numpy_array(item) for item in lst]
        return np.concatenate(items)
    else:
        return np.array(lst)