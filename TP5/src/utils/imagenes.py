from PIL import Image
import numpy as np

def imagen_a_matriz(imagen_path):
    # Cargar la imagen y convertirla a escala de grises
    imagen = Image.open(imagen_path).convert('L')

    # Convertir la imagen a una matriz numpy
    matriz = np.array(imagen)

    # Convertir la matriz a una matriz de 0 y 1
    matriz_binaria = (matriz > 128).astype(int)

    return matriz_binaria

path = 'CKGxZOs'

# Ruta de la imagen de entrada
imagen_path = '/home/gaston/Descargas/' + path + '.png'

# Obtener la matriz binaria
matriz_resultante = imagen_a_matriz(imagen_path)

i = 0
j = 0
# Imprimir la matriz resultante
for layer in matriz_resultante:
	j +=1
	if j == 15:
		j = 0
		for bit in layer:
			i+=1
			if i == 15:
				i = 0
				print(bit, "," , end='')


print("")
print("---------------------------")
print("")
print("---------------------------")

for layer in matriz_resultante:
	j +=1
	if j == 15:
		j = 0
		for bit in layer:
			i+=1
			if i == 15:
				i = 0
				print(bit, "" , end='')
		print("")
	
			
