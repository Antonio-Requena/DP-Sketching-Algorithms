import pandas as pd
import numpy as np
import random
import string

# Generar IDs únicos de usuario
def generate_user_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Generar combinaciones aleatorias de letras minúsculas para agregar ruido
def generate_random_string():
    length = random.randint(3, 8)  
    return ''.join(random.choices(string.ascii_lowercase, k=length))


# Palabras elegidas junto a sus proporciones
values = ["cool", "outfit", "brunch", "spoiler", "follower", "smartphone", "link", "feedback", "influencer", "hobby"]
probs = [0.18, 0.13, 0.14, 0.09, 0.11, 0.06, 0.11, 0.06, 0.07, 0.05]

# Tamaño del dataset (variante)
tamaños = [50,300,750,900,2500,15000,60000, 200000,350000, 1000000,2400000]

for N in tamaños:
    user_ids = set()
    while len(user_ids) < N:
        user_ids.add(generate_user_id())

    user_ids = list(user_ids)
    # Crear el dataset en formato csv
    data = []
    for user_id in user_ids:
        if random.random() < 0.1:  # 10% de probabilidad de añadir ruido
            value = generate_random_string()
        else:
            value = np.random.choice(values, p=probs)
        data.append([user_id, value])

    df = pd.DataFrame(data, columns=["user_id", "value"])

    df.to_csv(f'anglicismo_{N}.csv', index=False)