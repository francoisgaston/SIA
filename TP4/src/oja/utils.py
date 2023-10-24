import pandas as pd
import numpy as np


def read_input_normalize(input_file_path):
    df = pd.read_csv(input_file_path, header=None, skiprows=1)
    for column in df.columns:
        if column != 0:
            aux = df[column] - df[column].mean()
            df[column] = aux / df[column].std()
    aux = df.to_numpy()
    aux = np.delete(aux, 0, axis=1)
    names = pd.read_csv(input_file_path)
    names = names['Country']
    return aux, len(aux[0]), names