import numpy as np


def get_methyl_values_based_on_parac(parac):
    methyl_vals = np.random.uniform(0, 0.8, size=len(parac))

    for mother_index in range(len(parac)):
        if parac[mother_index] == 1:
            methyl_vals[mother_index] = methyl_vals[mother_index] + 0.2

    return methyl_vals


def get_ADD_from_parac(methyl_vals):
    return np.random.binomial(n=1, p=methyl_vals)
