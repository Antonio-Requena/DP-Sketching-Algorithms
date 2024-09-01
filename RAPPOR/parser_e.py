import pandas as pd
import numpy as np
import math

def calculate_new_values(row, col1, col2, col3):
    """Función para calcular los valores de las nuevas columnas basada en los valores de la fila."""
    h = 8
    try:
        # Obtén los valores de las columnas para esta fila
        val1 = float(row[col1])
        val2 = float(row[col2])
        val3 = float(row[col3])
        new_val1 = 2*h*math.log((1-(val1/2))/(val1/2))  
        new_val2 = h*math.log10((((1/2)*val1*(val2+val3)+(1-val1)*val3)*(1-((1/2)*val1*(val2+val3)+(1-val1)*val2)))/(((1/2)*val1*(val2+val3)+(1-val1)*val2)*(1-((1/2)*val1*(val2+val3)+(1-val1)*val3))))
    
        return pd.Series([round(new_val1,2), round(abs(new_val2),2)])
    except ValueError:
        # Manejo de valores que no se pueden convertir a float
        return pd.Series([None, None])  # O algún otro valor por defecto


def add_calculated_columns_to_csv(file_name, col1, col2, col3, new_col1, new_col2):
    h = 8
    # Lee el archivo CSV
    df = pd.read_csv(file_name)
        
    df[col1] = pd.to_numeric(df[col1], errors='coerce')
    df[col2] = pd.to_numeric(df[col2], errors='coerce')
    df[col3] = pd.to_numeric(df[col3], errors='coerce')
    df[[new_col1, new_col2]] = df.apply(lambda row: calculate_new_values(row, col1, col2, col3), axis=1)
    
    # Guarda el DataFrame modificado de nuevo en un archivo CSV
    df.to_csv(file_name, index=False)


# Ejemplo de uso
file_name = 'resultados_tests_PROB.csv'  # Nombre del archivo CSV
col1 = 'f'          # Nombre de la primera columna existente
col2 = 'p'          # Nombre de la segunda columna existente
col3 = 'q'          # Nombre de la tercera columna existente
new_col1 = 'e_PR' # Nombre de la primera nueva columna
new_col2 = 'e_IR' # Nombre de la segunda nueva columna

add_calculated_columns_to_csv(file_name, col1, col2, col3, new_col1, new_col2)