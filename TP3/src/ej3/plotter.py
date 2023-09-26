import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys

def graficar_errores_de_csv(ruta_csv):
    # Leer el archivo CSV en un DataFrame de Pandas
    df = pd.read_csv(ruta_csv)
    
    # Obtener IDs de configuración únicos
    ids_config_unicos = df['config_id'].unique()
    
    for config_id in ids_config_unicos:
        # Filtrar el DataFrame basado en config_id
        df_filtrado = df[df['config_id'] == config_id]
        
        # Extraer atributos de configuración para la anotación
        fila_muestra = df_filtrado.iloc[0]
        atributos_config = {
            'Capas Ocultas': fila_muestra['capas_ocultas'],
            'Activación': fila_muestra['activacion'],
            'Eta': fila_muestra['eta'],
            'Beta': fila_muestra['beta'],
            'Función de Activación': fila_muestra['activation'],
            'Función de Error': fila_muestra['error_function'],
            'Tamaño de Lote': fila_muestra['batch'],
            'Error Gaussiano': fila_muestra['noise_stddev'],
            'Augmentacion': fila_muestra['data_augmentation']
        }
        
        texto_anotacion = "<br>".join([f"{k}: {v}" for k, v in atributos_config.items()])
        
        # Ordenar por época
        df_filtrado = df_filtrado.sort_values('epoca')
        
        # Graficar usando Plotly
        fig = px.line(df_filtrado, x='epoca', y=['error_training', 'error_test'],
                      labels={'value': 'Error', 'epoca': 'Época'},
                      title=f"Error de Entrenamiento y Prueba para Config {config_id}")
        
        # Actualizar la disposición para hacer el eje x logarítmico
        fig.update_layout(xaxis_type="log", xaxis_title="Época Logarítmica")

        # Agregar la anotación con atributos de configuración
        fig.add_annotation(x=0, y=0, xref="paper", yref="paper",
                           text=texto_anotacion,
                           showarrow=False,
                           font=dict(size=10),
                           bordercolor="black",
                           borderwidth=1,
                           borderpad=4,
                           bgcolor="white",
                           opacity=0.8)
        
        fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)
    
    ruta_csv = sys.argv[1]
    graficar_errores_de_csv(ruta_csv)

