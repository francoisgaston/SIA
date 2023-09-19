import pandas as pd
import plotly.express as px
import sys

# Read your CSV file, replace the path accordingly
df = pd.read_csv("src/results/outfulldata_20230911184236.csv")

# Optionally, make id_config more readable. This example assumes 'id_config' is numerical.
# If it's a string that you want to modify, you can adjust this accordingly.
df['id_config_readable'] = df['id_config'].apply(lambda x: f"Configuración Optimizada para {x}")

# Group by 'id_config' and 'class' and calculate the mean 'fitness'
grouped_df = df.groupby(['id_config_readable', 'class']).fitness.mean().reset_index()

# Create the bar plot using Plotly Express
fig = px.bar(grouped_df, x='id_config_readable', y='fitness', color='class', barmode='group',
             labels={'fitness': 'Promedio de Aptitud', 'id_config_readable': 'ID de Configuración', 'class': 'Clase'},
             title='Promedio de Aptitud para Cada Clase y Configuración')

# Show the plot
fig.show()

