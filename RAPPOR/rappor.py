import math
import numpy as np
import random
import importlib.util
import os
import bloomfilter as bf
from sklearn import linear_model

# Enlace con la ruta para las utilidades (funciones de uso comun)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'utils.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

class Rappor:
    def __init__(self,k,m,f,p,q,dataset,domain):
        self.k = m # Número de bits por Bloom Filter (Concordancia en la notación con el pseudocódigo)
        self.f = f
        self.p = p
        self.q = q
        self.dataset = dataset
        self.domain = domain
        self.B = bf.BloomFilter(m,k)

    def cliente(self,value):
        B = self.B.get_bloomfilter(value)
        B_prima = [self.perturbar_bit_PL(bit,self.f) for bit in B]
        S =  [self.perturbar_bit_TL(bit,self.p,self.q) for bit in B_prima]
        return S
    
    def perturbar_bit_PL(self,bit,f):
        return random.choice([0,1]) if(random.random() < f) else bit
    
    def perturbar_bit_TL(self,bit,p,q):
        if bit == 1:
            return 1 if random.random() < q else 0
        else:
            return 1 if random.random() < p else 0
    
    def execute(self):
        Informes = []
        for d in self.dataset:
            Informes.append(self.cliente(d))
        
        X = self.crear_matriz_diseno()
        contadores_estimados = self.estimar_contadores(Informes)
        Y = np.mat(contadores_estimados).T
        estimacion = self.regresion_lasso(X,Y)

        print(estimacion)

    def crear_matriz_diseno(self):
        M = []
        for cadena in self.domain:
            M.append(self.B.get_bloomfilter(cadena))

        return np.mat(M).T
    
    def estimar_contadores(self,Informes):
        N = len(Informes)
        Informes = np.mat(Informes)
        contadores = np.array(np.sum(Informes,0))[0]
        contadores_estimados = [(c - (0.5*f*q + p-0.5*f*q)*N)/((1-f)*(q-p)) for c in contadores]
        return contadores_estimados
    
    def regresion_lasso(self, X,Y):
        reg = linear_model.Lasso(alpha=0.1, positive=True)
        reg.fit(np.asarray(X),np.asarray(Y))
        return reg.coef_



if __name__ == "__main__":

    # Parametros dependientes del caso de uso
    m = 64
    k = 6
    f = 0.5
    p = 0.5
    q = 0.75

    # Generamos un flujo artificial de N datos 
    N = 10**4
    dataset,df, domain = utils.create_dataset(N,'exp')

    R = Rappor(k,m,f,p,q,dataset,domain)
    R.execute()
    print(df)


