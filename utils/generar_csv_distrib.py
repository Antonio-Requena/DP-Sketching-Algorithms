import numpy as np
import pandas as pd
import random
import string

N = [50,300,900]
type = 'norm'

def generate_user_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

for n in N:

    if type == 'exp':
            valores = np.random.exponential(scale=2.0, size=n).astype(int)
    elif type == 'norm':
            valores = np.random.normal(loc=12, scale=2, size=n).astype(int)

    user_ids = set()
    while len(user_ids) < n:
        user_ids.add(generate_user_id())

    user_ids = list(user_ids)

    data = {'user_id': user_ids, 'value': valores}
    df = pd.DataFrame(data)
    df.to_csv(f'datasets/norm_distrib_{n}.csv', index=False)