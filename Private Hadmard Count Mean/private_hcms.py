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
        for d in self.dataset:
            w_i, j_i, l_i = self.cliente(d)
            self.actualizar_matriz_sketch(w_i,j_i,l_i)

        F_estimada = {}
        self.trasponer_M()
        for x in self.domain:
            F_estimada[x] = self.estimar_d(x)
        
        return F_estimada



if __name__ == "__main__":
    # Parametros dependientes del caso de uso
    k = 65536
    epsilon = 4
    m = 16

    # Generamos un flujo artificial de N datos 
    N = 10**4
    dataset,df, domain = utils.create_dataset(N,'small')


    HCMS = privateHCMS(epsilon,k,m,dataset,domain)
    f_estimada = HCMS.execute()
    utils.mostrar_resultados(df,f_estimada)


  
