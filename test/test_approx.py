import numpy as np
from unittest import TestCase

import random

import approx

import hchain

class TestGateCount(TestCase):

    def testGateCount(self):

        n_vals = [random.randint(1,100) for _ in range(3)]
        M_vals = [random.randint(1,200) for _ in range(3)]

        for n in n_vals:
            for M in M_vals:
                chain = hchain.HeisenbergChain(n, np.linspace(-1, 1, n))
                x = approx.gate_count(chain, M=M, permutation=[i for i in range(4 * n)])
                y = 8 * n * M - M - (n - 1) * M - M + 1
                self.assertEqual(x, y)

                x = approx.gate_count(chain, M=M)
                y = (5 * M + 1) * n
                self.assertEqual(x,y)

class TestFunctions(TestCase):

    def testRcopies(self):

        x = [1] * 10
        r = 30
        expected = [1/30]*300
        self.assertTrue(np.allclose(expected,approx.r_copies(x,r)))

    def testSuzuki(self):
        p_2 =  1/ (4 - 4 ** (1 / 3))
        x = [p_2, p_2, 1-4*p_2, p_2, p_2]
        self.assertTrue(np.allclose(x,approx.suzuki(2)))

        p_3 = 1/ (4 - 4 ** (1 / 5))
        y = [p_3 * p_2, p_3 * p_2, p_3 * (1 - 4 * p_2), p_3 * p_2, p_3 * p_2,
             p_3 * p_2, p_3 * p_2, p_3 * (1 - 4 * p_2), p_3 * p_2, p_3 * p_2,
             (1 - 4 * p_3) * p_2, (1 - 4*p_3) * p_2, (1 - 4 * p_3) * (1 - 4 * p_2),(1-4*p_3) * p_2, (1-4*p_3) * p_2,
             p_3 * p_2, p_3 * p_2, p_3 * (1 - 4 * p_2), p_3 * p_2, p_3 * p_2,
             p_3 * p_2, p_3 * p_2, p_3 * (1 - 4 * p_2), p_3 * p_2, p_3 * p_2]

        self.assertTrue(np.allclose(y, approx.suzuki(3)))

    def testExpandVals(self):
        for k in range(1,10):
            suz1 = approx.suzuki(k)
            suz2 = approx.expand_vals(approx.suzuki_vals(k))
            self.assertTrue(np.allclose(suz1, suz2))


