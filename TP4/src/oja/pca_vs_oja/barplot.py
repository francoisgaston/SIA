import os
import pandas as pd
import plotly.express as px


def main():
    directorio_csv = 'src/oja/results/'
    df_combined = pd.DataFrame()

    for archivo in os.listdir(directorio_csv):
        if archivo.startswith('pca_vs_oja_bar_') and archivo.endswith('.csv'):
            eta = archivo.split('_')[-1].replace('.csv', '')  # Extrae el valor de eta del nombre del archivo
            df = pd.read_csv(os.path.join(directorio_csv, archivo))
            df['Eta'] = eta
            df_combined = pd.concat([df_combined, df], ignore_index=True)

    print(df_combined)

    # Reformatea los datos utilizando melt para tener cada dato del encabezado en el eje X
    melted_data = df_combined.melt(id_vars=['Eta'], var_name='País', value_name='Valor')
    fig = px.bar(melted_data, x='País', y='Valor', color='Eta', labels={'Valor': 'PC1'}, barmode='group')
    fig.update_layout(title='PC1 para cada pais agrupado por eta')
    fig.update_traces(texttemplate='<b>%{text:.4f}</b>', textposition='outside')
    fig.show()


if __name__ == "__main__":
    main()
