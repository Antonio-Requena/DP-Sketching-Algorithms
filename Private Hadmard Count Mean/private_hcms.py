from sympy import primerange
import random
import numpy as np
import importlib.util
import os
import argparse
import time
from progress.bar import Bar
from tabulate import tabulate
import sys

# Enlace con la ruta para las utilidades (funciones de uso comun)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'utils.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

TEST_MODE = False

class privateHCMS:
    def __init__(self,epsilon,k,m, dataset, domain):
        # Inicialización de parámetros
        self.epsilon = epsilon
        self.k = k
        self.m = m
        self.dataset = dataset
        self.domain = domain
        self.H = self.hadamard_matrix(self.m)
        self.N = len(dataset)

        # Creación de la matriz de sketch
        self.M = np.zeros((self.k, self.m))

        # Definimos la familia de hashes independientes 3 a 3
        primos = list(primerange(10**6, 10**7))
        p = primos[random.randint(0, len(primos)-1)]
        self.hashes = utils.generate_hash_functions(self.k,p, 3,self.m)
    
    def hadamard_matrix(self,n):
        """
        Genera una matriz de Hadmard de tamaño mxm
        """
        if n == 1:
            return np.array([[1]])
        else:
            # Construcción recursiva
            h_half = self.hadamard_matrix(n // 2)
            h = np.block([[h_half, h_half], [h_half, -h_half]])
        return h

    def cliente(self,d):
        j = random.randint(0, self.k-1)
        v = np.full(self.m, 0)
        selected_hash = self.hashes[j]
        v[selected_hash(d)] = 1
        w = np.dot(self.H, v)
        l = random.randint(0, self.m-1)

        P_activo = np.exp(self.epsilon) / (np.exp(self.epsilon) + 1)
        if random.random() <= P_activo:
            b = 1
        else:
            b = -1
    
        return b*w[l],j,l

    def actualizar_matriz_sketch(self,w,j,l):
        c_e = (np.exp(self.epsilon/2)+1) / ((np.exp(self.epsilon/2))-1)
        x = self.k * c_e * w
        self.M[j,l] =  self.M[j,l] + x

    def trasponer_M(self):
        self.M = self.M @ np.transpose(self.H)

    def estimar_d(self,d):
        return (self.m/(self.m-1))*(1/self.k * np.sum([self.M[i,self.hashes[i](d)] for i in range(self.k)]) - self.N/self.m)
    
    def execute(self):
        bar = Bar('Procesando datos de los clientes', max=len(self.dataset), suffix='%(percent)d%%')
        t_cliente = 0
        size_cliente = 0
        t_act = 0
        for d in self.dataset:
            inicio = time.time()
            w_i, j_i, l_i = self.cliente(d)
            fin = time.time()
            size_cliente = sys.getsizeof(w_i) + sys.getsizeof(j_i) + sys.getsizeof(l_i)
            t_cliente += (fin - inicio) * 1000

            inicio = time.time()
            self.actualizar_matriz_sketch(w_i,j_i,l_i)
            fin = time.time()
            t_act += (fin - inicio) * 1000
            bar.next()
        bar.finish()
        t_cliente = t_cliente/len(self.dataset)
        t_act = t_act/len(self.dataset)

        F_estimada = {}
        self.trasponer_M()
        t_esti = 0
        bar = Bar('Obteniendo histograma de frecuencias estimadas', max=len(self.domain), suffix='%(percent)d%%')
        for x in self.domain:
            inicio = time.time()
            F_estimada[x] = self.estimar_d(x)
            fin = time.time()
            t_esti += (fin - inicio) * 1000
            bar.next()
        bar.finish()
        t_esti = t_esti/len(self.domain)

        # Tabla de tiempos de ejecución
        tiempos = [['Cliente (Por usuario)', str("{:.4f}".format(t_cliente)) + ' ms'],['Servidor (Actualizar matriz)',str("{:.4f}".format(t_act)) + ' ms'],['Servidor (Estimación individual)',str("{:.4f}".format(t_esti)) + ' ms'],['Ancho de banda',str("{:.3f}".format(size_cliente)) + ' kB']]
        
        return F_estimada, tiempos



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmo Private HADMARD Count Mean Sketch para la estimación de frecuencias a partir de un dominio conocido reduciendo el ancho de banda.")
    parser.add_argument("-k", type=int, required=True, help="Numero de funciones hash empleadas (Nº Filas en la matriz de sketch).")
    parser.add_argument("-m", type=int, required=True, help="Valor máximo del dominio de las funciones hash (Nº de columnas de la matriz de sketch)")
    parser.add_argument("-e", type=float, required=True, help="Valor de epsilon.")
    parser.add_argument("-d", type=str, required=True, help='Nombre del dataset empleado')
    parser.add_argument("--verbose_time", action="store_true", help="Se desea obtener los tiempos de ejecución de las funciones.")
    args = parser.parse_args()
    dataset,df, domain = utils.load_dataset(args.d)



    HCMS = privateHCMS(args.e,args.k,args.m,dataset,domain)
    f_estimada, tiempos = HCMS.execute()

    os.system('cls' if os.name == 'nt' else 'clear>/dev/null')
    if args.verbose_time: 
        if TEST_MODE: 
            for t in tiempos:
                print(f"{t[0]}: {t[1]}")
        else:
            tabla_tiempos = tabulate(tiempos, headers=["Algoritmo", "Tiempo de Ejecución"], tablefmt="pretty")
            print(tabla_tiempos + '\n')
    utils.mostrar_resultados(df,f_estimada)


  
