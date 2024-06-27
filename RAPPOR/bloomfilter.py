import math
import numpy as np
import random
from sympy import primerange
import importlib.util
import os

# Enlace con la ruta para las utilidades (funciones de uso comun)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'utils', 'utils.py'))
module_name = 'utils'

spec = importlib.util.spec_from_file_location(module_name, file_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


# Clase Bloom Filter adapatada al Algoritmo Rappor
class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k

        primos = list(primerange(10**6, 10**7))
        p = primos[random.randint(0, len(primos)-1)]
        self.H = utils.generate_hash_functions(self.k,p, self.k,self.m)
    
    def get_bloomfilter(self,data):
        B = np.zeros(self.m,int)
        for j in range(self.k):
            B[self.H[j](data)] = 1

        return B