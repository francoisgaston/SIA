
# TP1 SIA - Metodos de Busqueda

## Introducción

Trabajo práctico orientativo para la materia Sistemas de Inteligencia Artificial con el
objetivo de implementar diferentes metodos de búsqueda informados y no informados.

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

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución
### `src/main.py`
El programa `src/main.py` resuelve mapas del famoso juego [Sokoban](http://www.game-sokoban.com/) utilizando algoritmos de búsqueda informados y desinformados.
Para ello, mediante un archivo de configuración (que se encuentra detallado más adelante) se debe indicar el mapa, el algoritmo a utilizar y, en el caso de elegir un algortimo de búsqueda informado, la heurística a considerar.
Además, permite considerar los puntos del mapa que son considerados _deadlocks_, los cuales son casilleros que si llegan a ser ocupados por una caja, el mapa no tendrá solución.
Se ejecuta con el siguiente comando:
````sh
pipenv run python src/main.py [config_file]
````

#### Resultado
El programa puede devolver dos resultados:
- Si encuentra solución, imprime por un archivo txt una serie de _snapshots_ con los pasos a realizar para resolver el mapa
- Si no encuentra solución, imprime un mensaje de error por salida estándar

#### Configuración
El programa debe recibir por argumento el _path_ a un archivo JSON, el cual debe tener definido lo siguiente:
````json
{
  "map": "Path al archivo TXT que indica el map del sokoban - String",
  "algorithm": "Tipo de algoritmo para resolver el mapa - String",
  "heuristic": "Tipo de heuristica a utilizar para los algoritmos de búsqueda informados - String",
  "forbidden_points": "Booleano que indica si se deben considerar los puntos del mapa que son considerados deadlocks - ['YES', 'NO']",
  "output": "Path al archivo TXT donde se imprimirá la solución - String"
}
````

### `src/cruncher.py`
El programa `src/cruncher.py` permite ejecutar una serie de pruebas sobre un conjunto de mapas, algoritmos y heurísticas.
Como resultado, se obtiene un archivo CSV con los datos obtenidos. Al igual que `src/main.py`, se debe indicar un archivo de configuración JSON.
````sh
pipenv run python src/cruncher.py [config_file]
````

#### Resultado
El programa devuelve un archivo CSV con los siguientes datos:
````csv
Map, n-th map, Algorithm, Heuristic, Visited Count, End State Steps, Frontier Count, Execution Time
````
donde:
- `Map`: Nombre del mapa
- `n-th map`: Número de mapa ejecutado
- `Algorithm`: Algoritmo utilizado
- `Heuristic`: Heurística utilizada
- `Visited Count`: Cantidad de nodos visitados
- `End State Steps`: Cantidad de pasos para llegar al estado final
- `Frontier Count`: Cantidad de nodos en la frontera
- `Execution Time`: Tiempo de ejecución en segundos

#### Configuración
El programa debe recibir por argumento el _path_ a un archivo JSON, el cual debe tener definido lo siguiente:
````json
{
  "maps": "Arreglo de archivos TXT que definen los mapas del sokoban - String[]",
  "algorithms": "Lista de algoritmos a utilizar - String[]",
  "heuristics": "Lista de heurísticas a utilizar - String[]",
  "forbidden_points": "Booleano que indica si se deben considerar los puntos del mapa que son considerados deadlocks - ['YES', 'NO']",
  "output": "Path al archivo CSV donde se imprimirá la solución - String"
}
````

## Consideraciones
### Mapa
El archivo TXT:
- No debe tener lineas vacías 
- Debe respetar [este formato](http://www.sokobano.de/wiki/index.php?title=Level_format).

Para encontrar diferentes mapas puede recurrir a [game sokoban](http://www.game-sokoban.com/index.php)

### Algoritmo y heuristica
Tanto `algorithm` como `heuristic` solo toman ciertos valores predefinidos y *case-insensitive*:
- `algorithm`
  - "BFS": Implementado en `src/algorithms/bfs.py` 
  - "DFS": Implementado en `src/algorithms/dfs.py`
  - "GREEDY": Implementado en `src/algorithms/greedy.py`
  - "A*": Implementado en `src/algorithms/astar.py`
- `heuristic`
  - "DISTANCE": Implementado en `src/heuristics/distance_heuristic.py`
  - "PATH": Implementado en `src/heuristics/path_heuristic.py`
  - "COSINE": Implementado en `src/heuristics/cos_distance_heuristic.py`
  - "MAX_BOX": Implementado en `src/heuristics/max_box_heuristic.py`
  - "REC_PATH": Implementado en `src/heuristics/rec_path_heristic.py`
    
#### Notas
1. Para los algoritmos BFS y DFS, la heurística se ignora.
2. A los archivos de salida se les incluye un timestamp al nombre para evitar sobreescribir archivos.