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

e_values = [2]
e2_values = [6]  
k_values = [256]  # Añade más valores si es necesario
k2_values = [256]   # Añade más valores si es necesario
m_values = [64]  # Añade más valores si es necesario
data_values = ['anglicismo_50k']
T = [10]
data_values = [50,300,750,900,2500,15000,60000, 200000,350000, 1000000,2400000]
output_file = f'resultados_tests.txt'

bar = Bar('Procesando ejecuciones', max=len(e_values)*len(k_values)*len(T)*len(data_values)*len(k_values)*len(m_values), suffix='%(percent)d%%')
with open(output_file, 'w') as f:
    for n in data_values:
        DV = f'anglicismo_{n}'
        # Itera sobre todas las combinaciones de valores de los parámetros
        for k in k_values:
            for k2 in k2_values:
                for m in m_values:
                    for m2 in m_values:
                        for e in e_values:
                            for e2 in e2_values:
                                for t in T:
                                    # Construye el comando
                                    cmd = f'python3 -u private_sfp.py -e {e} -e2 {e2} -k {k} -k2 {k2} -m {m} -m2 {m2} -T {t} -d {DV} --verbose_time'
                                    print(cmd)
                                    # Ejecuta el comando y captura la salida
                                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                    stdout, stderr = process.communicate()
                                            
                                    # Escribe los parámetros en el archivo
                                    parametros = {'N':n}
                                    for key, value in parametros.items():
                                        f.write(f"{key}: {value}\n")
                                    f.write(stdout)
                                    f.write('\n'*2)
                                            
                                    bar.next()
            
    utils.parse_txt_to_csv(os.path.abspath(output_file))
    dir_name = os.path.dirname(os.path.abspath(output_file))
    destination_folder = os.path.join(dir_name, 'logs_tests')
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_file_path = os.path.join(destination_folder, output_file)
    shutil.move(output_file, destination_file_path)


bar.finish()