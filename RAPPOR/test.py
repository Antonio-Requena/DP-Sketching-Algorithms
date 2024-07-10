import subprocess
from progress.bar import Bar

# Define los valores de los parámetros a variar
m_values = [16,64,128,512]  
k_values = [1,6,32]
f_values = [0.5]  
p_values = [0.5]  
q_values = [0.75]    
N_values = [10000,500000]  
G_values = ['exp']  

# Archivo donde se almacenarán las salidas
output_file = 'resultados_tests.txt'

# Abre el archivo de salida
with open(output_file, 'w') as f:
    # Itera sobre todas las combinaciones de valores de los parámetros
    bar = Bar('Procesando ejecuciones', max=len(m_values)*len(k_values)*len(f_values)*len(p_values)*len(q_values)*len(N_values)*len(G_values), suffix='%(percent)d%%')
    for m in m_values:
        for k in k_values:
            for fv in f_values:
                for p in p_values:
                    for q in q_values:
                        for N in N_values:
                            for G in G_values:
                                # Construye el comando
                                cmd = f'python3 -u rappor.py -m {m} -k {k} -f {fv} -p {p} -q {q} -N {N} -G {G} --verbose_time  '
                                print(f'\nEjecutando: -m {m} -k {k} -f {fv} -p {p} -q {q} -N {N} -G {G}')
                                    
                                    # Ejecuta el comando y captura la salida
                                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                stdout, stderr = process.communicate()
                                    
                                # Escribe los parámetros en el archivo
                                f.write(f'Parámetros:  -m {m} -k {k} -f {fv} -p {p} -q {q} -N {N} -G {G}\n')
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