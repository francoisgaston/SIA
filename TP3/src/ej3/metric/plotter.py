import json
import sys
import pandas as pd
import plotly.graph_objects as go

from .metric import from_str as metric_from_str


def measure_macro(results, metric):
    """
    Returns the average of the results, using the macro average method
    sum of the metric for each class divided by the amount of classes
    """
    measure = 0
    for result in results:
        measure += metric.measure(result["tp"], result["tn"], result["fp"], result["fn"])
    return measure / len(results)


def measure_micro(results, metric):
    """
    Returns the average of the results, using the micro average method
    the metric is calculated using the sum of the tp, tn, fp and fn of all the classes
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for result in results:
        tp += result["tp"]
        tn += result["tn"]
        fp += result["fp"]
        fn += result["fn"]
    return metric.measure(tp, tn, fp, fn)


def measure(results, metric, avg_type):
    match avg_type.upper():
        case "MACRO":
            return measure_macro(results, metric)
        case "MICRO":
            return measure_micro(results, metric)
        case _:
            raise Exception("Invalid average type")


def measure_from_df(df, metric, avg_type):
    results = []
    for _, row in df.iterrows():
        results.append({"tp": row["tp"], "tn": row["tn"], "fp": row["fp"], "fn": row["fn"]})
    return measure(results, metric, avg_type)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Se necesitan los resultados de la matriz de confusión de entrenamiento y de testeo, y el archivo de "
              "configuración")
        exit(1)

    # Asumimos que el orden de los archivos es: train, test, config
    filename_1 = sys.argv[1].split("/")[-1].split(".")[0]
    filename_2 = sys.argv[2].split("/")[-1].split(".")[0]
    if "train" not in filename_1.split("_") or "test" not in filename_2.split("_"):
        print("El primer archivo debe ser el de entrenamiento y el segundo el de testeo")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as train_file, open(f"{sys.argv[2]}", "r") as test_file, open(f"{sys.argv[3]}",
                                                                                                   "r") as config_file:
        train_df = pd.read_csv(train_file)
        test_df = pd.read_csv(test_file)
        config = json.load(config_file)

        metric = metric_from_str(config["metric"]["name"])
        avg_type = config["metric"]["avg_type"]

        train_measures = []
        test_measures = []
        epochs = train_df["epoch"].unique()

        train_percentage = config["test_pct"] * 100
        test_percentage = 100 - train_percentage

        for epoch in epochs:
            train_measures.append(measure_from_df(train_df[train_df["epoch"] == epoch], metric, avg_type))
            test_measures.append(measure_from_df(test_df[test_df["epoch"] == epoch], metric, avg_type))

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=epochs, y=train_measures, mode='lines', name=f'Entrenamiento ({train_percentage}%)'))
        fig.add_trace(go.Scatter(x=epochs, y=test_measures, mode='lines', name=f'Testeo ({test_percentage}%)'))
        fig.add_trace(
            go.Scatter(
                name=f"{metric.name} final",
                x=[epochs[-1]],
                y=[train_measures[-1]],
                mode="markers+text",
                text=[f"<b>{metric.name} final<br>{round(train_measures[-1], 4)}</b>"],
                textposition="bottom center",
                textfont=dict(
                    size=14,
                    color="blue"
                ),
                marker=dict(
                    color="blue",
                    size=10,
                ),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                name=f"{metric.name} final",
                x=[epochs[-1]],
                y=[test_measures[-1]],
                mode="markers+text",
                text=[f"<b>{metric.name} final<br>{round(test_measures[-1], 4)}</b>"],
                textposition="top center",
                textfont=dict(
                    size=14,
                    color="red"
                ),
                marker=dict(
                    color="red",
                    size=10,
                ),
                showlegend=False,
            )
        )
        fig.update_layout(
            title=f"Evaluación de {metric.name} (promedio {avg_type}) para los conjuntos de entrenamiento y testeo"
                  f"<br><sup>Función de activación: {config['activation']}, con η = {config['n']}, β = {config['beta']}"
                  f" y batch = {config['batch']}<br>Arquitectura: {config['perceptrons_for_layers']}</sup>",
            xaxis_title="Época",
            yaxis_title=metric.name
        )
        fig.show()
