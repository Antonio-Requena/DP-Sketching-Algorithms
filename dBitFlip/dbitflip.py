import random
import math
import numpy as np
import os
import importlib.util
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

class dBitFlip:
    def __init__(self, dataset, epsilon, domain, d):
        self.dataset = dataset
        self.epsilon = epsilon
        self.domain = domain # domain es un vector que contiene diferentes valores posibles enviados por los usuarios
        if d > len(domain):
            raise ValueError("El valor d no puede superar |D|")
        else:
            self.d = d
        
        
    def cliente(self, value): # value corresponde al elemento que envia un usuario
        S = random.sample(self.domain, self.d)
        b = {}
        for j in S:
            if value == j:
                p = math.exp(self.epsilon / 2) / (math.exp(self.epsilon / 2) + 1)
            else:
                p= 1 / (math.exp(self.epsilon / 2) + 1)
            
            b_j = 1 if random.random() < p else 0
            b.update({j:b_j})
        
        return b
       
    def estimar_frecuencias(self, vectores_priv):

        n = len(vectores_priv)
        k = len(self.domain)
        frecuencia_estimacion = {}
        
        suma_frecuencias = {key: 0 for key in self.domain}
        
        for b in vectores_priv:
            for key, b_iv in b.items():
                suma_frecuencias[key] += (b_iv * (math.exp(self.epsilon / 2) + 1) - 1) / (math.exp(self.epsilon / 2) - 1)
        
        for key in self.domain:
            frecuencia_estimacion[key] = ((k / ( n * self.d)) * suma_frecuencias[key])*n # Corregimos el paso a frecuencias
        
        return frecuencia_estimacion
    
    def execute(self):
        bar = Bar('Procesando datos de los clientes', max=len(self.dataset), suffix='%(percent)d%%')
        vectores_priv = []
        t_cliente = 0
        for x in self.dataset:
            inicio = time.time()
            vectores_priv.append(self.cliente(x))
            fin = time.time()
            t_cliente += (fin - inicio) * 1000
            bar.next()
        bar.finish()
        t_cliente = t_cliente/len(self.dataset)
        
        t_server = 0
        print('\n' + 'Ejecutando algortimo del servidor' + '\n')
        inicio = time.time()
        F_estimada = self.estimar_frecuencias(vectores_priv)
        fin = time.time()
        t_server = (fin - inicio) * 1000

        # Tabla de tiempos de ejecución
        tiempos = [['Cliente (Por usuario)', str("{:.4f}".format(t_cliente)) + ' ms'],['Servidor (Estimar frecuencias)',str("{:.4f}".format(t_server)) + ' ms']]
        tabla_tiempos = tabulate(tiempos, headers=["Algoritmo", "Tiempo de Ejecución"], tablefmt="pretty")


        return F_estimada, tabla_tiempos


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Algoritmo dbitFlip para la estimación de frecuencias a partir de un dominio conocido.")
    parser.add_argument("-d", type=int, required=True, help="Numero de elementos del dominio enviados por los clientes.")
    parser.add_argument("-e", type=float, required=True, help="Valor de epsilon.")
    parser.add_argument("-D", type=str, required=True, help='Nombre del dataset empleado')
    parser.add_argument("--verbose_time", action="store_true", help="Se desea obtener los tiempos de ejecución de las funciones.")
    args = parser.parse_args()
    dataset,df, domain = utils.load_dataset(args.D)
   

    Bit = dBitFlip(dataset,args.e,domain,args.d)
    f_estimada, tiempos = Bit.execute()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    if(args.verbose_time): print(tiempos + '\n')
    utils.mostrar_resultados(df,f_estimada)

 
