import numpy as np
import pandas as pd
import random
import os
import string
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.stats import pearsonr

TEST_MODE = False#(ACTIVAR para test)


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

def load_dataset(csv_filename):
    """
    Carga un dataset desde un archivo CSV y devuelve los valores, el DataFrame y los valores únicos de 'value'.

    Args:
    - csv_filename (str): Nombre del archivo CSV que se encuentra en la carpeta 'datasets'.

    Returns:
    - valores (list): Dataset generado en formato lista.
    - df (DataFrame): Dataset generado en formato DataFrame (biblioteca Pandas).
    - unique_values (list): Valores únicos (dominio) del dataset.
    """
    # Construir la ruta completa al archivo CSV
    dataset_path =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils/datasets', csv_filename + '.csv'))

    # Cargar el dataset desde el archivo CSV
    df = pd.read_csv(dataset_path)
    df = df[['value']]
    
    # Obtener los valores como lista
    valores = df['value'].tolist()
    
    # Obtener los valores únicos
    unique_values = df['value'].unique().tolist()
    
    # Devolver los resultados
    return valores, df, unique_values

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
            diff = abs(f_real_num[elemento] - f_estimada_num[elemento])
            tabla_datos.append([elemento, frec_real, f"{porc_real:.3f}%", f"{frec_estimada:.2f}", f"{porc_estimada:.3f}%",f"{diff:.2f}"])
    

    # Cálculo de errores
    errores = [abs((f_real_num[key] - f_estimada_num[key])) for key in f_estimada_num]
    errores_mean = np.mean(errores)
    errores = np.sum(errores)
    max_f = max(f_real_num.values())
    min_f = min(f_real_num.values())

    mse = np.sum([(f_real_num[key] - f_estimada_num[key])**2 for key in f_estimada_num])/len(f_estimada_num)
    mse_norm = mse/(max_f-min_f)#np.sum([(f_real_num[key]/N - f_estimada_num[key]/N)**2 for key in f_estimada_num])/len(f_estimada_num)
    coef_pearson, _ = pearsonr(list(f_real_num.values()),list(f_estimada_num.values()))

    errores = [['Numero de errores', str("{:.2f}".format(errores))],['Numero de errores (media)', str("{:.2f}".format(errores_mean))],['Error porcentual', str("{:.2f}".format((errores_mean/N)*100) + '%')],['MSE', str("{:.2f}".format((mse)))], ['RMSE', str("{:.2f}".format((np.sqrt(mse))))],['MSE (Normalizado)', str("{:.2f}".format((mse_norm)))], ['RMSE (Normalizado)', str("{:.2f}".format((np.sqrt(mse_norm))))], ['Coeficiente correlacion Pearson', str("{:.4f}".format(coef_pearson))]]

    if TEST_MODE:
        errores = [['Media de errores', str("{:.2f}".format(errores_mean))],['Error porcentual', str("{:.2f}".format((errores_mean/N)*100) + '%')],['MSE', str("{:.2f}".format((mse)))], ['RMSE', str("{:.2f}".format((np.sqrt(mse))))],['MSE (Normalizado)', str("{:.2f}".format((mse_norm)))], ['RMSE (Normalizado)', str("{:.2f}".format((np.sqrt(mse_norm))))], ['Coeficiente correlacion Pearson', str("{:.4f}".format(coef_pearson))]]
        for error in errores:
            print(f"{error[0]}: {error[1]}")
    else:
        print("RESULTADOS OBTENIDOS")
        print(tabulate(tabla_datos, headers=["Elemento", "Frecuencia Real", "Porcentaje Real", "Frecuencia Estimada", "Porcentaje Estimado", "Diferencia en la estimacion"], tablefmt="pretty"))
        
        tabla_errores = tabulate(errores, tablefmt="pretty")
        print('\n'+tabla_errores)

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
