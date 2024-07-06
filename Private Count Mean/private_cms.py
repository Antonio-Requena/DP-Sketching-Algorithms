from sympy import primerange
import random
import numpy as np
import importlib.util
import os
import argparse
import time
from progress.bar import Bar
from tabulate import tabulate

# Enlace con la ruta para las utilidades (funciones de uso comun)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'utils.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)



class privateCMS:
    def __init__(self,epsilon,k,m, dataset, domain):
        # Inicialización de parámetros
        self.epsilon = epsilon
        self.k = k
        self.m = m
        self.dataset = dataset
        self.domain = domain
        self.N = len(dataset)

        # Creación de la matriz de sketch
        self.M = np.zeros((self.k, self.m))

        # Definimos la familia de hashes independientes 3 a 3
        primos = list(primerange(10**6, 10**7))
        p = primos[random.randint(0, len(primos)-1)]
        self.H = utils.generate_hash_functions(self.k,p, 3,self.m)
    
    def bernoulli_vector(self):
        b = np.random.binomial(1, (np.exp(self.epsilon/2)) / ((np.exp(self.epsilon/2)) + 1), self.m)
        b = 2 * b - 1  #Convertir los 0s en -1s
        return b

    def client(self,d):
        j = random.randint(0, self.k-1)
        v = np.full(self.m, -1)
        selected_hash = self.H[j]
        v[selected_hash(d)] = 1
        b = self.bernoulli_vector()
        v_aux = v*b
        return v_aux,j

    def actualizar_matriz_sketch(self,v,j):
        c_e = (np.exp(self.epsilon/2)+1) / ((np.exp(self.epsilon/2))-1)
        x = self.k * ((c_e/2) * v + (1/2) * np.ones_like(v))
        for i in range (self.m):
            self.M[j,i] =  self.M[j,i] + x[i]

    def estimar_d(self,d):
        sum_aux = 0
        for i in range(self.k):
            selected_hash = self.H[i]
            sum_aux += self.M[i,selected_hash(d)]
        
        f_estimada = (self.m/(self.m-1))*((sum_aux/self.k)-(self.N/self.m))
        return f_estimada
    
    def execute(self):
        bar = Bar('Procesando datos de los clientes', max=len(self.dataset), suffix='%(percent)d%%')
        t_cliente = 0
        t_act = 0
        for d in self.dataset:
            inicio = time.time()
            v_i, j_i = self.client(d)
            fin = time.time()
            t_cliente += (fin - inicio) * 1000

            inicio = time.time()
            self.actualizar_matriz_sketch(v_i,j_i)
            fin = time.time()
            t_act += (fin - inicio) * 1000
            bar.next()
        bar.finish()
        t_cliente = t_cliente/len(self.dataset)
        t_act = t_act/len(self.dataset)

        F_estimada = {}
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
        tiempos = [['Cliente (Por usuario)', str("{:.4f}".format(t_cliente)) + ' ms'],['Servidor (Actualizar matriz)',str("{:.4f}".format(t_act)) + ' ms'],['Servidor (Estimación individual)',str("{:.4f}".format(t_esti)) + ' ms']]
        tabla_tiempos = tabulate(tiempos, headers=["Algoritmo", "Tiempo de Ejecución"], tablefmt="pretty")


        return F_estimada, tabla_tiempos



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmo Private Count Mean Sketch para la estimación de frecuencias a partir de un dominio conocido.")
    parser.add_argument("-k", type=int, required=True, help="Numero de funciones hash empleadas (Nº Filas en la matriz de sketch).")
    parser.add_argument("-m", type=int, required=True, help="Valor máximo del dominio de las funciones hash (Nº de columnas de la matriz de sketch)")
    parser.add_argument("-e", type=float, required=True, help="Valor de epsilon.")
    parser.add_argument("-N", type=int, required=True, help='Numero de elementos del dataset generado.')
    parser.add_argument("-G", type=str, required=True, help='Tipo de generador [exp (exponencial), norm (normal), small (valores distribuidos en un dominio reducido)]')
    parser.add_argument("--verbose_time", action="store_true", help="Se desea obtener los tiempos de ejecución de las funciones.")
    args = parser.parse_args()
    dataset,df, domain = utils.create_dataset(args.N,args.G)


    PCMS = privateCMS(args.e,args.k,args.m,dataset,domain)
    f_estimada, tiempos = PCMS.execute()

    os.system('cls' if os.name == 'nt' else 'clear')
    if(args.verbose_time): print(tiempos + '\n')
    utils.mostrar_resultados(df,f_estimada)


  
