import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, ScalarFormatter


def porcentaje(x, pos):
    return f'{x}%'

# Crea el formateador usando la función definida
formatter = FuncFormatter(porcentaje)

# Función para cargar los datos de los archivos CSV
def cargar_datos(nombre_archivo):
    return pd.read_csv(nombre_archivo)

def convertir_porcentajes(columna):
    return columna.str.rstrip('%').astype('float') 


# Cargar los datos de los dos archivos CSV
archivo1 = 'COSTEN_resultados_tests.csv'
archivo2 = 'COSTEN_resultados_tests copy.csv'

datos1 = cargar_datos(archivo1)
datos2 = cargar_datos(archivo2)

datos1['Error porcentual'] = convertir_porcentajes(datos1['Error porcentual'])
datos2['Error porcentual'] = convertir_porcentajes(datos2['Error porcentual'])

# Crear la figura y los subplots
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

V_dependiente = 'N'
col1 = 'Error porcentual'

a1 = 'Private Count Mean Sketch'
a2 = 'Private Hadmard Count Mean Sketch'


plt.plot(datos1[0:5][V_dependiente].astype('int') 
, datos1[0:5][col1], label=a1, color='b')
plt.plot(datos2[0:5][V_dependiente].astype('int') , datos2[0:5][col1], label=a2, color='r')

plt.rcParams.update({'font.size': 20})
plt.grid(True)
plt.gca().xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.gca().ticklabel_format(style='plain', axis='x')
plt.gca().yaxis.set_major_formatter(formatter)
plt.xlabel('N')
plt.ylabel('Error porcentual')
plt.legend()

ax.tick_params(axis='both', which='major', labelsize=14)

# Añade las etiquetas y la leyenda
ax.set_xlabel('X Label', fontsize=14)
ax.set_ylabel('Y Label', fontsize=14)
ax.legend(fontsize=14)

# Ajustar el layout
plt.tight_layout()

# Mostrar las gráficas
plt.show()