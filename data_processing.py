import pyarrow.parquet as pq
import pandas as pd
import numpy as np

def data_processing(file):
    data = pq.read_table(file)
    donnees = data.to_pandas()
    espace = donnees[['x', 'y','z']].to_numpy()
    return espace



