import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
# Configurar la fuente a Latin Modern Roman
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# Definir los nombres de los archivos y los tamaños de los datasets
files = {
    'PCMS': ['resultados_tests_exp_distrib_750.csv','resultados_tests_exp_distrib_50k.csv','resultados_tests_exp_distrib_1M.csv'],
    'HPCMS': ['resultados_tests_exp_distrib_750_H.csv','resultados_tests_exp_distrib_50k_H.csv','resultados_tests_exp_distrib_1M_H.csv']
    
}
sizes = ['750','50k','1M']

# Leer los datos
data = {algo: [pd.read_csv(file) for file in files[algo]] for algo in files}
METRICA = 'Media de errores'
# Crear subplots
fig, axs = plt.subplots(2, 3, figsize=(18, 6))


# Definir los nombres de los algoritmos para los títulos
algorithm_names = ['PCMS', 'HCMS']
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))

# Crear los mapas de calor
for row, algo in enumerate(files):
    for col, size in enumerate(sizes):
        ax = axs[row, col]
        df = data[algo][col]
        
        # Extraer los valores de k, m y la métrica
        k = df['k'].values
        m = df['m'].values
        metric = df[METRICA].values
        
        # Obtener valores únicos y ordenarlos
        k_unique = np.unique(k)
        m_unique = np.unique(m)
        k_min, k_max = np.min(k), np.max(k)
        m_min, m_max = np.min(m), np.max(m)

        # Crear una malla para k y m
        k_grid, m_grid = np.meshgrid(k_unique, m_unique)
        
        # Crear una matriz de la métrica correspondiente
        metric_grid = np.zeros_like(k_grid, dtype=float)
        for i, ki in enumerate(k_unique):
            for j, mj in enumerate(m_unique):
                if not df[(df['k'] == ki) & (df['m'] == mj)].empty:
                    metric_grid[j, i] = df[(df['k'] == ki) & (df['m'] == mj)][METRICA].values[0]
                else:
                    metric_grid[j, i] = np.nan  # Usar NaN para valores faltantes
        
        # Definir el colormap y la normalización para cada gráfico
        cmap = plt.get_cmap('viridis')  # Puedes elegir otro colormap si lo prefieres
        norm = mcolors.Normalize(vmin=np.nanmin(metric_grid), vmax=np.nanmax(metric_grid))
        
        # Crear el mapa de calor
        c = ax.pcolormesh(k_grid, m_grid, metric_grid, shading='auto', cmap=cmap, norm=norm)
        
        # Añadir una barra de colores independiente para cada gráfico
        cbar = fig.colorbar(c, ax=ax, orientation='vertical')
        cbar.set_label(METRICA, fontsize=10)
        cbar.ax.tick_params(labelsize=8)

        # Configurar los límites y las marcas de los ejes
        ax.set_xlim([k_min, k_max])
        ax.set_ylim([m_min, m_max])
        
        # Configurar el gráfico
        ax.set_title(f'{algo}\n($\\varepsilon = 2$, N = {size})', fontsize=10)
        ax.set_xlabel('k', fontsize=8)
        ax.set_ylabel('m', fontsize=8)
        
        # Ajustar la rotación y el tamaño de las etiquetas de los ejes
        ax.tick_params(axis='both', which='major', labelsize=8)

# Ajustar layout
plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.show()