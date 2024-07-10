import subprocess
from progress.bar import Bar

# Define los valores de los parámetros a variar
e_values = [0.5,2,4,8]  # Añade más valores si es necesario
k_values = [128,32768,65536]  # Añade más valores si es necesario
m_values = [128,1024]  # Añade más valores si es necesario
N_values = [10000,500000]  # Añade más valores si es necesario
G_values = ['exp']  # Añade más valores si es necesario

# Archivo donde se almacenarán las salidas
output_file = 'resultados_tests.txt'

# Abre el archivo de salida
with open(output_file, 'w') as f:
    # Itera sobre todas las combinaciones de valores de los parámetros
    bar = Bar('Procesando ejecuciones', max=len(e_values)*len(k_values)*len(m_values)*len(N_values)*len(G_values), suffix='%(percent)d%%')
    for e in e_values:
        for k in k_values:
            for m in m_values:
                for N in N_values:
                    for G in G_values:
                        # Construye el comando
                        cmd = f'python3 -u private_cms.py -k {k} -m {m} -e {e} -N {N} -G {G} --verbose_time'
                        print(f'\nEjecutando: -e {e} -k {k} -m {m} -N {N} -G {G}')
                        
                        # Ejecuta el comando y captura la salida
                        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        stdout, stderr = process.communicate()
                        
                        # Escribe los parámetros en el archivo
                        f.write(f'Parámetros: -e {e} -k {k} -m {m} -N {N} -G {G}\n')
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