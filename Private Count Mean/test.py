import subprocess
from progress.bar import Bar

# Define los valores de los parámetros a variar
e_values = [2]  # Añade más valores si es necesario
k_values = [16,128,1024,32768,65536]  # Añade más valores si es necesario
m_values = [16,64,256,1024]  # Añade más valores si es necesario
data_values = ['exp_distrib_1M','exp_distrib_50k','exp_distrib_750']


for DV in data_values:
    output_file = f'resultados_tests_{DV}.txt'
    bar = Bar('Procesando ejecuciones', max=len(e_values)*len(k_values)*len(m_values)*len(data_values), suffix='%(percent)d%%')
    with open(output_file, 'w') as f:
        # Itera sobre todas las combinaciones de valores de los parámetros
        for k in k_values:
            for m in m_values:
                for e in e_values:
                    # Construye el comando
                    cmd = f'python3 -u private_cms.py -k {k} -m {m} -e {e} -d {DV} --verbose_time'
                    print(f'\nEjecutando: -e {e} -k {k} -m {m} -d {DV}')
                            
                    # Ejecuta el comando y captura la salida
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                            
                    # Escribe los parámetros en el archivo
                    parametros = {'e':e,'k':k,'m':m}
                    for key, value in parametros.items():
                        f.write(f"{key}: {value}\n")
                    f.write(stdout)
                    f.write('\n'*2)
                            
                    bar.next()

bar.finish()