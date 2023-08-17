
# TP1 SIA - Metodos de Busqueda

## Introducción

Trabajo práctico orientativo para la materia Sistemas de Inteligencia Artificial con el
objetivo de implementar diferentes metodos de busqueda informados o no informados.

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
El programa `src/main.py` resuelve mapas del famoso juego [Sokoban](http://www.game-sokoban.com/) utilizando algoritmos de búsqueda informados y desinformados.
Para ello, mediante un archivo de configuración (que se encuentra detallado más adelante) se debe indicar el mapa, el algoritmo a utilizar y, en el caso de elegir un algortimo de búsqueda informado, la heurística a considerar.
Se ejecuta con el siguiente comando:
````sh
pipenv run python src/main.py [config_file]
````

### Resultado
El programa puede devolver dos resultados:
- Si encuentra solución, imprime por salida estándar una serie de _snapshots_ con los pasos a realizar para resolver el mapa

### Configuración
El programa debe recibir por argumento el _path_ a un archivo JSON, el cual debe tener definido lo siguiente:
````json
{
  "map": "Path al archivo TXT que indica el map del sokoban - String",
  "algorithm": "Tipo de algoritmo para resolver el mapa - String",
  "heuristic": "Tipo de heuristica a utilizar para los algoritmos de búsqueda informados - String"
}
````
#### Mapa
El archivo TXT:
- No debe tener lineas vacías 
- Debe respetar [este formato](http://www.sokobano.de/wiki/index.php?title=Level_format).

#### Algoritmo y heuristica
Tanto `algorithm` como `heuristic` solo toman ciertos valores predefinidos y *case-insensitive*:
- `algorithm`
  - "BFS": Implementado en `src/algorithms/bfs.py` 
  - "DFS": Implementado en `src/algorithms/dfs.py`
  - "GREEDY": Implementado en `src/algorithms/greedy.py`
  - "A*": Implementado en `src/algorithms/astar.py`
- `heuristic`
  - "DISTANCE": Implementado en `src/heuristics/distance_heuristic.py`
  - "PATH": Implementado en `src/heuristics/path_heuristic.py`
Para los algoritmos BFS y DFS, la heurística se ignora.
