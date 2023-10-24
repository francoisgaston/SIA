import sys
import json
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from ..utils import read_input


def main():
    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        # lectura de input sin nombres de paises
        data, names, headers = read_input(config["input"])

        # Normalizacion de los valores
        scaling = StandardScaler()
        scaling.fit(data)
        Scaled_data = scaling.transform(data)

        # Analisis de proporciones de varianza
        principal = PCA()
        principal.fit(Scaled_data)
        variances = principal.explained_variance_ratio_

        # Grafico de proporciones de varianza
        df = pd.DataFrame({'varianza': variances,
                           'componentes': [f"PC{i}" for i in range(1, len(variances) + 1)]})
        fig = px.bar(df, x='componentes', y='varianza', color='varianza', color_continuous_scale='bluered')
        fig.update_layout(xaxis_title="Componentes principales",
                            yaxis_title="% de varianza",
                            title="Proporciones de varianza explicadas por cada componente principal",
                            coloraxis_showscale=False,
                            yaxis=dict(
                                tickformat=".0%",
                            ))
        fig.update_traces(textfont_size=16, textposition='outside', text=variances, texttemplate='<b>%{text:.2%}</b>')

        output = f"{config['output']}variance_prop.html"
        fig.write_html(output)


if __name__ == "__main__":
    main()
