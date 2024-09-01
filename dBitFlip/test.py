import subprocess
from progress.bar import Bar
import os
import importlib
import shutil

# Enlace con la ruta para generar el csv
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'parser_csv.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


# Define los valores de los parámetros a variar
e_values = [1]  # Añade más valores si es necesario
d_values = [4]  # Añade más valores si es necesario
data_values = [50,300,750,900,2500,'15k',60000, '200k',350000, 1000000,2400000]
# Archivo donde se almacenarán las salidas
output_file = 'resultados_tests.txt'

# Abre el archivo de salida
with open(output_file, 'w') as f:
    # Itera sobre todas las combinaciones de valores de los parámetros
    bar = Bar('Procesando ejecuciones', max=len(e_values)*len(d_values)*len(data_values), suffix='%(percent)d%%')
    for e in e_values:
        for d in d_values:
                for n in data_values:
                    DV = f'norm_distrib_{n}'
                    cmd = f'python3 -u dbitflip.py -d {d} -e {e} -D {DV} --verbose_time'
                        
                    # Ejecuta el comando y captura la salida
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                    
                    
                    # Ejecuta el comando y captura la salida
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                                    
                    # Escribe los parámetros en el archivo
                    parametros = {'N':n,'d':d,'e':e}
                    for key, value in parametros.items():
                            f.write(f"{key}: {value}\n")
                    f.write(stdout)
                    f.write('\n'*2)
                                    
                    bar.next()
    bar.finish()

utils.parse_txt_to_csv(os.path.abspath(output_file))
dir_name = os.path.dirname(os.path.abspath(output_file))
destination_folder = os.path.join(dir_name, 'logs_tests')
    
    # Crear la carpeta de destino si no existe
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

destination_file_path = os.path.join(destination_folder, output_file)
shutil.move(output_file, destination_file_path)
