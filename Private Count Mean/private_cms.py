from sympy import primerange
import random
import numpy as np
import importlib.util
import os

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
        for d in self.dataset:
            v_i, j_i = self.client(d)
            self.actualizar_matriz_sketch(v_i,j_i)

        F_estimada = {}
        for x in self.domain:
            F_estimada[x] = self.estimar_d(x)
        
        return F_estimada



if __name__ == "__main__":
    # Parametros dependientes del caso de uso
    k = 65536
    epsilon = 4
    m = 1024

    # Generamos un flujo artificial de N datos 
    N = 10**4
    dataset,df, domain = utils.create_dataset(N,'exp')


    PCMS = privateCMS(epsilon,k,m,dataset,domain)
    f_estimada = PCMS.execute()

    utils.mostrar_resultados(df,f_estimada)


  
