import numpy as np
import time


def mult_norm(ind):
    summ = sum(ind)
    assert(summ != 0)
    return np.array(ind)/summ


def shift_norm(ind):
    summ = sum(ind)
    return np.array([ind[i] + (1-summ)/len(ind) for i in range(len(ind))])

