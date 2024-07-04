import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.stats import pearsonr
import math

def create_dataset(N:int, type:str)->tuple[list,pd.DataFrame,list]:
    """
    Creación de un dataset para la estimación de frecuencias.

    Args:
        N (int): Número de elementos en el dataset.
        type (string): Tipo de generador [exp (exponencial), norm (normal), small (valores distribuidos en un dominio reducido)]

    Returns:
        valores (list): Dataset generado en formato lista.
        df (Dataframe): Dataset generado en formato dataframe (libreria Pandas)
        unique_values (list): Valores únicos (dominio) del dataset

    Examples:
        >>> create_dataset(10**6, 'exp')
        >>> create_dataset(1000, 'small')
    """
    # Generar valores exponenciales
    if type == 'exp':
        valores = np.random.exponential(scale=2.0, size=N).astype(int)
    elif type == 'norm':
        valores = np.random.normal(loc=12, scale=2, size=N).astype(int)
    elif type == 'small':
        elementos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        frecuencias = [0.29, 0.19, 0.15, 0.12, 0.1,0.08, 0.05, 0.02]
        dataset = np.random.choice(elementos, size=N, p=frecuencias)
        valores = dataset.tolist()
        np.random.shuffle(valores)
    
    # Crear un DataFrame
    df = pd.DataFrame({
        'value': valores,
    })

    unique_values = df['value'].unique().tolist()
    unique_values.sort()
    return valores,df, unique_values


def generate_hash_functions(k, p, c,m):
    """
Generación de un conjunto de k funciones hash (D->m) c-independientes entre si.
    Parámetros:
        c (int) (Número de coeficientes): Cuando se define una familia de funciones c-independientes
        k (int) (Número de funciones hash)
        p (int) (Número primo grande): Necesario para la construccion de las funciones hash
        m (int) (Valor máximo del dominio al que mapean las funciones hash)

    Salida:
        hash_functions (list): Conjunto con la familia de k funciones hash

"""
    hash_functions = []
    for _ in range(k):
        # c coeficientes aleatorios modulo p
        coefficients = [random.randint(1, p-1) for _ in range(c)]
        # Construimos las funciones hash como expresiones labda
        hash_func = lambda x, coeffs=coefficients, p=p: (sum((coeffs[i] * (hash(x) ** i)) % p for i in range(c)) % p)%m
        hash_functions.append(hash_func)
    return hash_functions

def mostrar_resultados(frecuencia_real:pd.DataFrame, f_estimada_num: dict):
    N = frecuencia_real.shape[0]

    # Cálculos relacionados con las frecuencias reales
    f = frecuencia_real['value'].value_counts()
    f_real_num = (f.sort_index()).to_dict()
    f_real_percent = ((f*100/N).sort_index()).to_dict()
    
    # Preparar los datos para su posterior impresión por pantalla
    tabla_datos = []
    for elemento in f_real_num:
        if elemento in f_estimada_num:
            frec_real = f_real_num[elemento]
            porc_real = f_real_percent[elemento]
            frec_estimada = f_estimada_num[elemento]
            porc_estimada = (frec_estimada /N) * 100
            diff = (f_real_num[elemento] - f_estimada_num[elemento])
            tabla_datos.append([elemento, frec_real, f"{porc_real}%", f"{frec_estimada:.2f}", f"{porc_estimada:.2f}%",f"{diff:.2f}"])
    
    print("RESULTADOS OBTENIDOS")
    print(tabulate(tabla_datos, headers=["Elemento", "Frecuencia Real", "Porcentaje Real", "Frecuencia Estimada", "Porcentaje Estimado", "Diferencia en la estimacion"], tablefmt="pretty"))

    # Cálculo de errores
    errores = {key: math.pow((f_real_num[key] - f_estimada_num[key]),2) for key in f_estimada_num}
    MSE = np.mean(list(errores.values()))/(np.mean(list(f_real_num.values()))**2)
    RMSE = math.sqrt(MSE)
    errores = [abs((f_real_num[key] - f_estimada_num[key])/f_real_num[key]) for key in f_estimada_num]

    MAE = np.mean(errores)
    MAPE = np.mean(errores)*100
    coef_pearson, _ = pearsonr(list(f_real_num.values()),list(f_estimada_num.values()))

    errores = [['MSE normalizado', str("{:.4f}".format(MSE))],['RMSE normalizado', str("{:.4f}".format(RMSE))],['MAE', str("{:.4f}".format(MAE))],['MAPE', str("{:.4f}".format(MAPE))], ['Coeficiente correlacion Pearson', str("{:.4f}".format(coef_pearson))]]
    tabla_errores = tabulate(errores, tablefmt="pretty")

    print(tabla_errores)

    
    # Representación visual
    data = {
        'Frecuencia Real': f_real_num,
        'Frecuencia Estimada': f_estimada_num
    }
    df = pd.DataFrame(data)
    
    # Crear la gráfica
    df.plot(kind='bar', figsize=(10, 6))
    plt.title('Comparación de Frecuencias Reales y Estimadas')
    plt.xlabel('Elementos')
    plt.ylabel('Número de Ocurrencias')
    plt.xticks(rotation=0)
    plt.legend(loc='best')
    plt.show()