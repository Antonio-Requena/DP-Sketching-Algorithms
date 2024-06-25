from sympy import primerange
import random
import numpy as np
import importlib.util
import os
import hashlib
import string
import re
import csv
from collections import Counter
from progress.bar import Bar
import argparse

# Enlace con la ruta para las utilidades (funciones de uso comun)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'utils.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

# Enlace con la ruta de Private Count Mean
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'Private Count Mean', 'private_cms.py'))
module_name = 'pcms'

spec = importlib.util.spec_from_file_location(module_name, file_path)
pcms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pcms)

class privateSPF:
    def __init__(self,epsilon,epsilon_prima,k,k_prima,m,m_prima,dataset,T):
        # Inicialización de parámetros
        self.epsilon = epsilon
        self.epsilon_2 = epsilon_prima
        self.k = k
        self.k_2 = k_prima
        self.m = m
        self.m_2 = m_prima
        self.dataset = dataset
        self.N = len(self.dataset)
        self.posiciones = [1,3,5,7,9]
        self.T = T
        self.CMS_2 = [None]*len(self.posiciones)

        # Se inicializan las instancias del algoritmo Private Count Mean Sketch
        self.CMS = pcms.privateCMS(self.epsilon,self.k,self.m,dataset,None)
        for i in range(len(self.posiciones)):
            self.CMS_2[i] = pcms.privateCMS(self.epsilon_2,self.k_2,self.m_2,dataset,None)

        self.h =  lambda s: int(hashlib.md5(s.encode()).hexdigest(), 16) % 256
    
    def cliente(self,s):
        l = random.choice(self.posiciones)
        r = str(self.h(s)) + s[l-1:l+1]
        return self.CMS_2[self.posiciones.index(l)].client(r), self.CMS.client(s),l
    
    def servidor(self,alpha, beta, l):
        self.CMS_2[self.posiciones.index(l)].actualizar_matriz_sketch(alpha[0],alpha[1])
        self.CMS.actualizar_matriz_sketch(beta[0],beta[1])

    def separar_hash(self,clave):
        match = re.match(r"(\d+)([a-zA\s]{2})", clave)
        if match:
            hash = match.group(1)
            caracteres = match.group(2)
            return hash, caracteres
        else:
            raise ValueError(f"Clave no válida: {clave}")

    def generar_diccionario(self,T):
        X = {}
        Q_l = [None]*len(self.posiciones)
        Q_w = [[]]*256
        alfabeto = string.ascii_lowercase + ' ' # abcdefghijklmnopqrstuvwxyz + espacio
        combinaciones = [a + b for a in alfabeto for b in alfabeto]
        bar = Bar('Generando el diccionario', max=len(self.posiciones)*256, suffix='%(percent)d%%')

        for l in self.posiciones:
            pos = self.posiciones.index(l)

            # Generar el diccionario auxiliar
            dict = {}
            # Iterar sobre los valores w de 0 a 255
            for w in range(256):
                bar.next()
                for c in combinaciones:
                    clave = str(w) + c
                    dict[clave] = self.CMS_2[pos].estimar_d(clave)

            # Seleccionamos las T más frecuentes
            Q_l[pos] = sorted(dict, key=dict.get, reverse=True)[:T]

        bar.finish()

        for w in range(256):
            q_l =  [[] for _ in range(len(self.posiciones))]
            for q in Q_l:
                i = Q_l.index(q)
                for clave in q:
                    aux = self.separar_hash(clave)
                    if aux[0] == str(w):
                        q_l[i].append(aux[1])
            
            Q_w[w] = [  # Generamos las posibles concatenaciones q1 || q3 || ... || q9 : w || ql
                q1 + q3 + q5 + q7 + q9
                for q1 in q_l[0]
                for q3 in q_l[1]
                for q5 in q_l[2]
                for q7 in q_l[3]
                for q9 in q_l[4]
            ]
            
            for x in Q_w[w]:
                X[x] = self.CMS.estimar_d(x)
        
        return X

    def execute(self):
        bar = Bar('Procesando datos de los clientes', max=len(self.dataset), suffix='%(percent)d%%')
        for d in self.dataset:
            alpha, beta, l = self.cliente(d)
            self.servidor(alpha, beta, l)
            bar.next()
        bar.finish()

        X = self.generar_diccionario(self.T)

        X = {k: v for k, v in sorted(X.items(), key=lambda item: item[1], reverse=True)}
        for clave, valor in X.items():
            print(f"{clave}: {valor}")
                

def generar_csv(N):
    palabras = [ "chiquillo","guasa","jartarse","jabato","despeinao","tasca","mantecaito","enquinao","zurrapa","achuchar","quillo","picha","nonina", "antoje"]
    probabilidades = np.random.exponential(scale=1.0, size=len(palabras))
    probabilidades = probabilidades / probabilidades.sum()
    dic = np.random.choice(palabras, size=N, p=probabilidades)

    with open('andalusian_words.csv', mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['value'])  # Escribir encabezado de la columna
        
        # Escribir N filas de datos
        for d in dic:
            writer.writerow([d])

def cargar_csv(nombre_archivo):
    dataset = []
    
    with open(nombre_archivo, mode='r', newline='') as archivo_csv:
        reader = csv.reader(archivo_csv)
        next(reader)  # Saltar el encabezado
        
        for row in reader:
            valor =  row[0][:10].ljust(10) # Normalizamos las cadenas
            dataset.append(valor)
    
    return dataset, dict(Counter(dataset))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Algoritmo Sequence Fragment Puzzle para la estimación de frecuencias a partir de un diccionario desconocido.")
    
    # Añadimos los argumentos requeridos
    parser.add_argument("-e", type=int, required=True, help="Epsilon.")
    parser.add_argument("-e2", type=int, required=True, help="Epsilon prima.")
    parser.add_argument("-k", type=int, required=True, help="k (Número de filas de la matriz de sketch para la secuencia).")
    parser.add_argument("-k2", type=int, required=True, help="k prima (Número de filas de la matriz de sketch para las piezas)")
    parser.add_argument("-m", type=int, required=True, help="m (Número de columnas de la matriz de sketch para la secuencia).")
    parser.add_argument("-m2", type=int, required=True, help="m prima (Número de columnas de la matriz de sketch para las piezas).")
    parser.add_argument("-T", type=int, required=True, help='Umbral que acota superiormente la cantidad de cadenas estimadas a generar.')
    parser.add_argument("-N", type=int, required=True, help='Numero de elementos del dataset generado.')
    parser.add_argument("-vs","--verbose_time", action="store_true", help="Se desea obtener los tiempos de ejecución de las funciones.")
    
    args = parser.parse_args()

    # Generamos un flujo artificial de N datos y lo almacenamos en un CSV
    N = 10**4
    generar_csv(args.N)
    dataset,frecuencias = cargar_csv('andalusian_words.csv')
    
    print('Configurando parámetros iniciales... ')
 
    SPF = privateSPF(args.e,args.e2,args.k,args.k2,args.m,args.m2,dataset,args.T)
    SPF.execute()

    print(frecuencias)

    


  