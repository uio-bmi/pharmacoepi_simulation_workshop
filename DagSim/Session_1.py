import numpy as np

n_samples = 100

mothers = np.random.binomial(1, 0.5, size=100)

methyl_vals = np.random.uniform(0, 0.8, size=n_samples)

for mother_index in range(n_samples):
    if mothers[mother_index] == 1:
        methyl_vals[mother_index] = methyl_vals[mother_index] + 0.2

ADD_values = np.random.binomial(n=1, p=methyl_vals)
