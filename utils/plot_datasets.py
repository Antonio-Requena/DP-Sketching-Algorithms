import pandas as pd
import matplotlib.pyplot as plt

def graficar_frecuencias(csv_filename):
 # Leer el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(csv_filename)

    # Contar las frecuencias de cada valor único en la columna 'value'
    frecuencias = df['value'].value_counts()

    # Ordenar los valores y frecuencias
    frecuencias = frecuencias.sort_index()

    # Configurar el gráfico de barras
    plt.figure(figsize=(12, 6))  # Tamaño del gráfico
    ax = frecuencias.plot(kind='bar', color='peachpuff', edgecolor='black')  # Gráfico de barras
    plt.xlabel('Elemento')
    plt.ylabel('Frecuencia real')
    plt.xticks(rotation=45)  # Rotar etiquetas del eje x para mejor visualización
    # Mostrar el número de veces que aparece cada valor encima de la barra
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout()  # Ajustar diseño
    plt.show()

def plotear_frecuencias(dataset_filename):
    df = pd.read_csv(dataset_filename)

    # Calcular las frecuencias de cada elemento
    frecuencias = df['value'].value_counts()

    # Calcular el porcentaje total de ocurrencias
    total_ocurrencias = frecuencias.sum()

    # Determinar el umbral para 'Otras (Ruido)' (0.5% del total)
    umbral = 0.001 * total_ocurrencias

    # Identificar las cadenas que tienen menos de 0.5% del total de ocurrencias
    otras = frecuencias[frecuencias < umbral]

    # Agruparlas bajo la categoría 'Otras (Ruido)'
    frecuencias_otras = otras.sum()
    frecuencias_restantes = frecuencias[frecuencias >= umbral]

    frecuencias_restantes = frecuencias_restantes.sort_values(ascending=False)
    # Crear una nueva serie con 'Otras (Ruido)'
    frecuencias_agrupadas = pd.concat([frecuencias_restantes, pd.Series([frecuencias_otras], index=['Otras (Ruido)'])])

    # Configurar el gráfico
    plt.figure(figsize=(12, 6))  # Tamaño del gráfico
    # Definir colores
    colores = ['skyblue'] * len(frecuencias_agrupadas)
    # Cambiar el color del elemento destacado
    if 'Otras (Ruido)' in frecuencias_agrupadas.index:
        indice_destacado = frecuencias_agrupadas.index.get_loc('Otras (Ruido)')
        colores[indice_destacado] = 'salmon'  # Cambiar el color a salmon para el elemento destacado
    
    # Graficar las barras con colores personalizados
    plt.bar(frecuencias_agrupadas.index, frecuencias_agrupadas.values, color=colores, edgecolor='black')  
    plt.xlabel('Cadena')
    plt.ylabel('Frecuencia Real')
    plt.xticks(rotation=45)  # Rotar etiquetas del eje x para mejor visualización

    plt.tight_layout()  # Ajustar diseño
    plt.show()


plotear_frecuencias('datasets/anglicismo_50k.csv')