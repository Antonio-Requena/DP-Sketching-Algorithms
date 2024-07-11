import numpy as np
import pandas as pd
import random
import string


N = 750
type = 'exp'

if type == 'exp':
        valores = np.random.exponential(scale=2.0, size=N).astype(int)
elif type == 'norm':
        valores = np.random.normal(loc=12, scale=2, size=N).astype(int)


def generate_user_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

user_ids = set()
while len(user_ids) < N:
    user_ids.add(generate_user_id())

user_ids = list(user_ids)

data = {'user_id': user_ids, 'value': valores}
df = pd.DataFrame(data)
df.to_csv('datasets/exp_distrib_750.csv', index=False)