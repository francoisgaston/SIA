import pandas as pd
import plotly.graph_objects as go
import sys

def graficar_errores_de_csv(ruta_csv):
    # Leer el archivo CSV en un DataFrame de Pandas
    df = pd.read_csv(ruta_csv)
    
    # Obtener IDs de configuración únicos
    ids_config_unicos = df['config_id'].unique()

    # Inicializar figura
    fig = go.Figure()

    # Loop through unique config_ids
    for config_id in ids_config_unicos:
        # Filtrar el DataFrame basado en config_id
        df_filtrado = df[df['config_id'] == config_id]

        # Extraer atributos relevantes
        fila_muestra = df_filtrado.iloc[0]
        augmentacion = fila_muestra['data_augmentation']
        stddev = fila_muestra['noise_stddev']

        # Construir el texto simplificado para la anotación/etiqueta
        if(augmentacion):
          texto_anotacion = f"Augmentado"
        else:
          texto_anotacion = f"No augmentado"

        # Ordenar por época
        df_filtrado = df_filtrado.sort_values('epoca')

        # Agregar líneas al gráfico
        fig.add_trace(go.Scatter(x=df_filtrado['epoca'], y=df_filtrado['error_training'],
                                 mode='lines', name=f"Training {config_id} ({texto_anotacion})"))
        fig.add_trace(go.Scatter(x=df_filtrado['epoca'], y=df_filtrado['error_test'],
                                 mode='lines', name=f"Test {config_id} ({texto_anotacion})"))

    # Actualizar etiquetas y título
    fig.update_layout(xaxis_title="Época Logarítmica",
                      yaxis_title="Error",
                      title="Comparacion Errores con y sin augmentacion de datos",
                      xaxis_type="log")

    # Mostrar figura
    fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)
    
    ruta_csv = sys.argv[1]
    graficar_errores_de_csv(ruta_csv)

