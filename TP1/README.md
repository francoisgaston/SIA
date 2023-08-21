
# TP1 SIA - Métodos de Busqueda

<img src="docs/solucion.gif" width="200" alt="Sokoban GIF">


## Introducción

Trabajo práctico orientativo para la materia Sistemas de Inteligencia Artificial con el
objetivo de implementar diferentes métodos de búsqueda informados y no informados.

[Enunciado](docs/SIA_TP1.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en el directorio raiz, ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual.

## Ejecución
### `src/main.py`
El programa `src/main.py` resuelve mapas del famoso juego [Sokoban](http://www.game-sokoban.com/) utilizando algoritmos de búsqueda informados y desinformados.
Para ello, mediante un archivo de configuración (que se encuentra detallado más adelante) se debe indicar el mapa, el algoritmo a utilizar y, en el caso de elegir un algortimo de búsqueda informado, la heurística a considerar.
Además, permite considerar los puntos del mapa llamados _deadlocks_, los cuales son casilleros que si llegan a ser ocupados por una caja, el mapa no tendrá solución.
Se ejecuta con el siguiente comando:
````sh
pipenv run python src/main.py [config_file]
````

#### Resultado
El programa puede devolver dos resultados:
- Si encuentra solución, imprime por salida estándar estadísticas de la solución 
  - Tiempo de ejecución
  - Cantidad de nodos visitados
  - Cantidad de nodos en el conjunto frontera
  - Cantidad de pasos para llegar a la solución

  
Dependiendo del campo _realistic_ definido en el archivo de configuración, la secuencia de estados que lleva a la solución se guarda:
- True: Como una animación GIF 
- False: En un archivo TXT que almacena la serie de _snapshots_ con los pasos a realizar para resolver el mapa


- Si no encuentra solución, no imprime la solución ni cantidad de pasos a realizar.

#### Configuración
El programa debe recibir por argumento el _path_ a un archivo JSON, el cual debe tener definido lo siguiente:
````json
{
  "map": "Path al archivo TXT que indica el mapa del sokoban - String",
  "algorithm": "Tipo de algoritmo para resolver el mapa - String",
  "heuristic": "Tipo de heuristica a utilizar para los algoritmos de búsqueda informados - String",
  "forbidden_points": "Booleano que indica si se deben considerar los puntos del mapa que son considerados deadlocks - Boolean",
  "output": "Nombre del archivo que se guardará en src/results - String",
  "realistic": "Booleano que indica si se debe generar una animación GIF con la solución - Boolean"
}
````
Los valores disponibles para los campos `algorithm` y `heuristic` se detallan más adelante.

### `src/cruncher.py`
El programa `src/cruncher.py` permite ejecutar una serie de pruebas sobre un conjunto de mapas, algoritmos y heurísticas.
Como resultado, se obtiene un archivo CSV con los datos obtenidos. Al igual que `src/main.py`, se debe indicar un archivo de configuración JSON.
````sh
pipenv run python src/cruncher.py [config_file]
````

#### Resultado
El programa devuelve un archivo CSV con los siguientes datos:
````csv
Map, Steps, Algorithm, Heuristic, Visited Count, End State Steps, Frontier Count, Execution Time
````
donde:
- `Map`: Path al archivo del mapa
- `Steps`: Cantidad de pasos para llegar a la solución óptima
- `Algorithm`: Algoritmo utilizado
- `Heuristic`: Heurística utilizada (útil si el algoritmo es informado)
- `Visited Count`: Cantidad de nodos visitados
- `End State Steps`: Cantidad de pasos para llegar al estado final
- `Frontier Count`: Cantidad de nodos en la frontera
- `Execution Time`: Tiempo de ejecución en segundos

#### Configuración
El programa debe recibir por argumento el _path_ a un archivo JSON, el cual debe tener definido lo siguiente:
````json
{
  "maps": "Arreglo de [Archivo TXT de mapa, Cantidad de pasos de la solución óptima] - [String, Integer][]",
  "algorithm": "Lista de algoritmos a utilizar - String[]",
  "heuristic": "Lista de heurísticas a utilizar - String[]",
  "forbidden_points": "Booleano que indica si se deben considerar los puntos del mapa que son considerados deadlocks - Boolean",
  "repetitions": "Cantidad de veces que se debe repetir la ejecución para cada combinación de mapa, algoritmo y heurística (si es informado) - Integer",
  "output": "Path al archivo CSV donde se imprimirá los datos - String"
}
````

## Consideraciones
### Mapa
El archivo TXT:
- No debe tener lineas vacías 
- Debe respetar [este formato](http://www.sokobano.de/wiki/index.php?title=Level_format).

Para encontrar diferentes mapas puede recurrir a [Sokoban](http://www.game-sokoban.com/index.php).

### Algoritmo y heuristica
Tanto `algorithm` como `heuristic` solo toman ciertos valores predefinidos y *case-insensitive*:
- `algorithm`
  - "BFS" (**Default**): Implementado en `src/algorithms/bfs.py` 
  - "DFS": Implementado en `src/algorithms/dfs.py`
  - "GREEDY": Implementado en `src/algorithms/greedy.py`
  - "A*": Implementado en `src/algorithms/astar.py`
- `heuristic`
  - "DISTANCE" (**Default**): Implementado en `src/heuristics/distance_heuristic.py`
  - "PATH": Implementado en `src/heuristics/path_heuristic.py`
  - "COSINE": Implementado en `src/heuristics/cos_distance_heuristic.py`
  - "MAX_BOX": Implementado en `src/heuristics/max_box_heuristic.py`
    
#### Notas
1. Para los algoritmos BFS y DFS, la heurística se ignora.
2. A los archivos de salida se les incluye un timestamp al nombre para evitar sobreescribir archivos.