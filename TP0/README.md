
# TP0 SIA - Análisis de Datos

## Introducción

Trabajo práctico orientativo para la materia Sistemas de Inteligencia Artificial con el
objetivo de evaluar la función de captura de un Pokemon.

[Enunciado](docs/SIA_TP0.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en el directorio raiz, ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución
### Scripts
#### main.py
Script genérico para ejecutar la función de captura de Pokemon.
- **Input**: Archivo JSON de configuración
    ```json
    {
      "pokeball": "Pokeball name - String",
      "output": "Output CSV file name - String",
      "times": "Number of times to run the simulation - Integer",
      "noise": "Normalized noise to add to the function - Float [0, 1]",
      "pokemon": {
        "name": "Pokemon name - String",
        "level": "Pokemon level - Integer",
        "current_hp": "Pokemon current HP - Float [0, 1]",
        "status_effect": "StatusEffect constant name - String"
      }
    }
    ```
- **Output**: Archivo CSV con los resultados de la simulación
    ```csv
    attempt_success, catch_rate
    ```
    - <ins>attempt_success</ins>: Indica si el intento de captura fue exitoso o no - Boolean
    - <ins>catch_rate</ins>: Probabilidad de captura del Pokemon - Float [0, 1]
    
- **Ejecución**
    ```sh
    pipenv run python main.py [config_file]
    ```
    
  
#### main1a.py

#### main1b.py

#### main2a.py

#### plot/plot2a.py

#### main2b.py

#### plot/plot2b.py

#### main2c.py
Ejecuta la función de captura de Pokemon realizando varias simulaciones para cada nivel del Pokemon, de 1 a 100. 
Por cada nivel, se ejecuta varias veces la función una cantidad de intentos, es decir se ejecuta la función N veces y esto se repite M veces por nivel. Por cada N ejecuciones, se calcula la efectividad promedio, a partir de la cantidad de intentos exitosos sobre la cantidad de intentos totales de esa serie.
- **Input**: Archivo JSON de configuración
    ```json
    {
      "pokemons": "Array of Pokemon names - String[]",
      "pokeball": "Pokeball name - String",
      "current_hp": "Pokemon current HP - Float [0, 1]",
      "status_effect": "StatusEffect constant name - String",
      "output": "Output CSV file name - String",
      "times_per_level": "M, Number of times to run the simulation for each level - Integer",
      "catch_tries_per_time": "N, Number of catch tries per time per level - Integer",
      "noise": "Normalized noise to add to the function - Float [0, 1]"
    }
    ```
- **Output**: Archivo CSV con los resultados de la simulación
    ```csv
    pokemon, level, effectiveness_avg
    ```
    - <ins>pokemon</ins>: Nombre del Pokemon - String
    - <ins>level</ins>: Nivel del Pokemon - Integer
    - <ins>effectiveness_avg</ins>: Efectividad promedio de captura del Pokemon - Float [0, 1]
    
- **Ejecución**
    ```sh
    pipenv run python main2c.py [config_file]
    ```
    
#### plot/plot2c.py   
Realiza un gráfico de lineas a partir de los resultados obtenidos en `main2c.py`.
- **Input**: 
  - Archivo CSV generado por `main2c.py`
  - Archivo JSON de configuración
      ```json
      {
        "pokemons": "Array of Pokemon names to graph - String[]",
        "output": "Output HTML file name - String",
        "graph": {
          "title": "Graph title - String",
          "xaxis_title": "X axis title - String",
          "yaxis_title": "Y axis title - String",
          "decimal_places": "Number of decimal places to round the values - Integer"
        } 
      }
      ```
- **Output**: Archivo HTML con el gráfico realizado por `Plotly`
    
- **Ejecución**
    ```sh
    pipenv run python plot/2c/plot2c.py [main2c_generated_csv_file] [config_file]
    ```

