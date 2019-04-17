import numpy as np

from cachetools import cached, LFUCache
from scipy.linalg import expm
from term import XXTerm, YYTerm, ZZTerm, ZTerm

import settings

cache_size = 0
if settings.enable_cache():
    cache_size = 100

cache = LFUCache(maxsize=cache_size)


class HeisenbergChain:
    """
    A Heisenberg chain of n qubits, with vector v coupled to Z.
    """

    def __init__(self, n, v):

        self.n = n
        self.v = v
        assert(len(v) == n)

        self.terms = []

        for i in range(1, self.n + 1):
            for term in [XXTerm, YYTerm, ZZTerm]:
                self.terms.append(term(i, self.n))

            self.terms.append(ZTerm(i, self.n, v[i - 1]))

    @cached(cache)
    def matrix(self):
        h = np.zeros((2**self.n, 2**self.n)).astype(complex)
        for term in self.terms:
            h += term.matrix()
        return h

    @cached(cache)
    def exponential(self, coefficient):
        return expm(coefficient * self.matrix())

    def num_terms(self):
        return len(self.terms)

    def __str__(self):
        return 'n: ' + str(self.n) + ', v: ' + str(self.v)

    def __hash__(self):
        return str(self).__hash__()


