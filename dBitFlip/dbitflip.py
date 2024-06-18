import random
import math
import numpy as np

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
        
        # Inicializar la suma de las frecuencias ajustadas
        suma_frecuencias = {key: 0 for key in self.domain}
        
        # Calcular la suma de las frecuencias ajustadas
        for b in vectores_priv:
            for key, b_iv in b.items():
                suma_frecuencias[key] += (b_iv * (math.exp(self.epsilon / 2) + 1) - 1) / (math.exp(self.epsilon / 2) - 1)
        
        # Calcular la estimación de la frecuencia para cada elemento del dominio
        for key in self.domain:
            frecuencia_estimacion[key] = (k / ( n * self.d)) * suma_frecuencias[key]
        
        return frecuencia_estimacion
    
    def execute(self):
        vectores_priv = []
        for x in self.dataset:
            vectores_priv.append(self.cliente(x))
        
        F_estimada = self.estimar_frecuencias(vectores_priv)
        return F_estimada


if __name__ == '__main__':
    # PARÁMETROS
    N = 300000
    epsilon = 2
    d = 2


    dataset,df, domain = gen.create_dataset(N,'small')
   
    frecuencias = df['value'].value_counts()
    frecuencias = (frecuencias/N).sort_index()
    frecuencias = frecuencias.to_dict()
    print(frecuencias)

    Bit = dBitFlip(dataset,epsilon,domain,d)
    F_estimada = Bit.execute()

    print(F_estimada)

 
