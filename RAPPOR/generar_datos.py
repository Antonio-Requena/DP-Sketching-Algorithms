import numpy as np

def generar_archivo_exponencial(nombre_archivo, n, lambda_param=1.0):
    """
    Genera un archivo de texto con n filas, cada una contiene 5 números generados
    a partir de una distribución exponencial con parámetro lambda_param y separados
    por tabuladores.

    :param nombre_archivo: Nombre del archivo de salida.
    :param n: Número de filas a generar.
    :param lambda_param: Parámetro lambda de la distribución exponencial.
    """
    # Generar los datos
    datos = np.random.exponential(scale=1/lambda_param, size=(n, 7))
    datos = datos.astype(int)
    # Escribir los datos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        for fila in datos:
            linea = '\t'.join(map(str, fila))
            archivo.write(linea + '\n')

# Uso de la función
nombre_archivo = 'datos_exponenciales.txt'
n = 100000  # Número de filas
lambda_param = 0.75  # Parámetro lambda de la distribución exponencial
generar_archivo_exponencial(nombre_archivo, n, lambda_param)
