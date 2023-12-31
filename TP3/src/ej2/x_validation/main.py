import json
import os
import sys
import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame

from ...activation import from_str as activation_from_str
from ...utils.Function import Function
from ...utils.write_csv import append_row_to_csv, create_csv, get_filename, write_csv
from ..main import run_perceptron, format_data
from .on_epoch import OnEpoch
from .on_epoch import from_str as on_epoch_from_str


def k_separate(data: DataFrame, k: int):
    """
    Returns a list of k folds, each fold is a DataFrame
    """
    if k > len(data):
        raise Exception("k debe ser menor o igual a la cantidad de datos")

    shuffled = data.sample(frac=1).reset_index(drop=True)
    folds = []
    for i in range(k):
        folds.append(shuffled[i::k].reset_index(drop=True))
    return folds


def k_fold_iteration(train_data: ndarray, test_data: ndarray, train_expected: ndarray, test_expected: ndarray,
                     config: dict):
    """
    Performs a single iteration of the k-fold cross validation
    Saves the results to a csv file
    Returns the minimum error of the test data
    """
    activation_function = activation_from_str(string=config['activation'], beta=config["beta"])
    onEpoch = on_epoch_from_str(string=config['x_validation']['on_epoch'], activation_function=activation_function)
    min_error = sys.float_info.max

    def on_epoch(w: ndarray, epoch: int):
        nonlocal min_error
        train_error, test_error = onEpoch.exec(w, epoch, train_data, train_expected, test_data, test_expected)
        min_error = onEpoch.final_test_error()
        row = [epoch] + w.tolist() + [train_error, test_error]
        append_row_to_csv(config["filename"], row)

    run_perceptron(
        config=config,
        data=train_data,
        expected=train_expected,
        on_epoch=on_epoch
    )
    return min_error


def format_fold(fold: DataFrame, activation_function: Function):
    """
    Formats a fold into a dictionary with the data and expected values
    """
    data, expected = format_data(fold, activation_function)
    return {
        "data": data,
        "expected": expected
    }


def k_fold(config: dict, k: int, df: DataFrame):
    """
    Performs a k-fold cross validation
    """
    activation_function = activation_from_str(string=config['activation'], beta=config["beta"])
    # Se obtiene cada fold de la forma {data: ndarray, expected: ndarray}
    folds = k_separate(df, k)
    folds = [format_fold(fold, activation_function) for fold in folds]
    min_errors = []  # Lista de los mínimos errores de testeo de cada fold
    filename_prefix = config['output'] + config['data'].split("/")[-1].split(".")[0]
    filenames = []  # Lista de los nombres de los archivos csv de cada fold
    # Los headers de los csv son: Epoch, w0, w1, ..., wn, train_error, test_error
    headers = ["Epoch"] + ["w" + str(i) for i in range(len(folds[0]["data"][0]))] + ["train_error", "test_error"]
    for i in range(k):
        print("Testeando fold ", i+1, " de ", k, " folds")
        train_data = np.array([])
        train_expected = np.array([])
        # Se obtienen los datos de entrenamiento y de testeo
        for j in range(k):
            # Los datos de entrenamiento son todos los folds menos el fold actual
            if j != i:
                train_data = np.concatenate((train_data, folds[j]["data"])) if len(train_data) != 0 else folds[j][
                    "data"]
                train_expected = np.concatenate((train_expected, folds[j]["expected"])) if len(train_expected) != 0 else \
                folds[j]["expected"]
        # El fold actual es el de testeo
        test_data = folds[i]["data"]
        # print(test_data.shape)
        test_expected = folds[i]["expected"]
        tmp_filename_prefix = filename_prefix.split("/")
        tmp_filename_prefix.insert(-1, "tmp")
        filename = "/".join(tmp_filename_prefix) + "_fold_" + str(i)
        # Se crea el archivo csv para guardar los resultados de este fold
        filenames.append(create_csv(filename, headers))
        config["filename"] = filenames[i]
        # Se realiza la iteración del k-fold
        min_error = k_fold_iteration(train_data, test_data, train_expected, test_expected, config)
        # Se guarda el mínimo error de testeo de este fold
        min_errors.append(min_error)
        print("El mínimo error de testeo del fold ", i+1, " fue: ", min_error)
    # Se obtiene el índice del fold con el mínimo error de testeo
    best_fold_idx = min_errors.index(min(min_errors))
    # Se eliminan los archivos csv de los folds que no son el de mínimo error
    # y se renombra el archivo csv del fold de mínimo error a un nombre genérico
    for i in range(k):
        if i != best_fold_idx:
            os.remove(filenames[i])
        else:
            data_filename_prefix = filename_prefix.split("/")
            data_filename_prefix.insert(-1, "data")
            data_filename = get_filename("/".join(data_filename_prefix))
            os.makedirs(os.path.dirname(data_filename), exist_ok=True)
            os.rename(filenames[i], data_filename)
    headers = ["x" + str(i) for i in range(len(folds[0]["data"][0]))] + ["y"]
    # Se guarda el conjunto de datos de entrenamiento en un csv
    rows = []
    for i in range(k):
        if i != best_fold_idx:
            for j in range(len(folds[i]["data"])):
                rows.append(folds[i]["data"][j].tolist() + [folds[i]["expected"][j]])
    train_filename_prefix = filename_prefix.split("/")
    train_filename_prefix.insert(-1, "train")
    write_csv("/".join(train_filename_prefix), headers, rows)
    # Se guarda el conjunto de datos de testeo en un csv
    rows = []
    for j in range(len(folds[best_fold_idx]["data"])):
        rows.append(folds[best_fold_idx]["data"][j].tolist() + [folds[best_fold_idx]["expected"][j]])
    test_filename_prefix = filename_prefix.split("/")
    test_filename_prefix.insert(-1, "test")
    write_csv("/".join(test_filename_prefix), headers, rows)
    # Se retorna el mínimo error de testeo
    return min_errors[best_fold_idx]


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        with open(config['data'], 'r', newline='') as data_file:
            df = pd.read_csv(data_file)
        k = config['x_validation']["k_fold"]
        min_error = k_fold(config, k, df)
        print("El mínimo error de testeo fue: ", min_error)
