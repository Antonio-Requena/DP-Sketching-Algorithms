import subprocess
from progress.bar import Bar
import csv
import re

# Define los valores de los parámetros a variar
e_values = [0.5,2,4,8]  # Añade más valores si es necesario
d_values = [1,2,4,8]  # Añade más valores si es necesario
data_values = ['exp_distrib_1M','exp_distrib_50k','exp_distrib_750']  # Añade más valores si es necesario

# Archivo donde se almacenarán las salidas
output_file = 'resultados_tests.txt'

# Abre el archivo de salida
with open(output_file, 'w') as f:
    # Itera sobre todas las combinaciones de valores de los parámetros
    bar = Bar('Procesando ejecuciones', max=len(e_values)*len(d_values)*len(data_values), suffix='%(percent)d%%')
    for e in e_values:
        for d in d_values:
                for D in data_values:
                    cmd = f'python3 -u dbitflip.py -d {d} -e {e} -D {D} --verbose_time'
                        
                    # Ejecuta el comando y captura la salida
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                        
                    # Escribe los parámetros en el archivo
                    f.write(f'Parámetros: -e {e} -d {d} Dataset: {D}\n')
                    f.write('Salida:\n')
                    f.write(stdout)
                    f.write('\n')
                    
                    # Escribe cualquier error en el archivo (opcional)
                    if stderr:
                        f.write('Errores:\n')
                        f.write(stderr)
                        f.write('\n')
                        
                    # Escribe una separación entre diferentes ejecuciones
                    f.write('\n' + '-'*80 + '\n\n')
                    bar.next()

    bar.finish()