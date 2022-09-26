import numpy as np


def get_methyl_values_based_on_parac(parac):
    methyl_val = np.random.uniform(0, 0.8)

    if parac == 1:
        methyl_val = methyl_val + 0.2
    return methyl_val


def get_ADD_from_methyl_val(methyl_val):
    ADD = np.random.binomial(n=1, p=methyl_val)
    return ADD


def split_based_on_ADD(ADD):
    if ADD == 1:
        return "ADD_positive"
    else:
        return "ADD_negative"
