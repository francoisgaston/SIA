import pandas as pd


def read_input(input_file_path):
    df = pd.read_csv(input_file_path)
    headers = df.columns.tolist()
    names = df['Country']
    selected_columns = df.loc[:, df.columns != 'Country']
    selected_columns = selected_columns.iloc[0:]
    aux = selected_columns.to_numpy()
    return aux, names, headers
