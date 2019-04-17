import numpy as np
from unittest import TestCase


import gates as gates
import hchain as hchain

from hchain import XXTerm, YYTerm, ZZTerm, ZTerm


# all for 2 qubits
x1x2 = np.array([[0,   0,   0,   1],   [0,   0,   1,   0], [0,   1,   0,   0],   [1,   0,   0,   0]])

x1x2_exp_r2 = np.array([[0.8776,  0.0000,  0.0000,  0.4794j],
                        [0.0000,  0.8776,  0.4794j, 0.0000],
                        [0.0000,  0.4794j, 0.8776,  0.0000],
                        [0.4794j, 0.0000,  0.0000,  0.8776]])

y2y1_exp_r10 = np.array([[0.9950 + 0.0000j, 0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.0000 - 0.0998j],
                         [0.0000 + 0.0000j, 0.9950 + 0.0000j, 0.0000 + 0.0998j, 0.0000 + 0.0000j],
                         [0.0000 + 0.0000j, 0.0000 + 0.0998j, 0.9950 + 0.0000j, 0.0000 + 0.0000j],
                         [0.0000 - 0.0998j, 0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.9950 + 0.0000j]])

z1_exp_r5 = np.array([[0.9992 + 0.0400j, 0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.0000 + 0.0000j],
                     [0.0000 + 0.0000j, 0.9992 + 0.0400j, 0.0000 + 0.0000j, 0.0000 + 0.0000j],
                     [0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.9992 - 0.0400j, 0.0000 + 0.0000j],
                     [0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.0000 + 0.0000j, 0.9992 - 0.0400j]])

# Canonical segment for hchain with n=2, v = [-.5, .5]
v_n2 = [-0.5, 0.5]
canonicalterms_n2 = [ XXTerm(1, 2), YYTerm(1, 2), ZZTerm(1, 2), ZTerm(1, 2, v_n2[0]),
                         XXTerm(2, 2), YYTerm(2, 2), ZZTerm(2, 2), ZTerm(2, 2, v_n2[1])]


y1y2 = np.array([[0,   0,   0,  -1],   [0,   0,   1,   0], [0,  -1,   0,   0],   [0,   0,   0,   1]])
z1z2 = np.array([[1,   0,   0,   0],   [0,  -1,   0,   0], [0,   0,  -1,   0],   [1,   0,   0,   0]])

x2x1 = np.array([[0,   0,   0,   1],   [0,   0,   1,   0], [0,   1,   0,   0],   [1,   0,   0,   0]])

y2y1 = np.array([[0,   0,   0,  -1],   [0,   0,   1,   0], [0,  -1,   0,   0],   [0,   0,   0,   1]])

z2z1 = np.array([[1,   0,   0,   0],   [0,  -1,   0,   0], [0,   0,  -1,   0],   [0,   0,   0,   1]])


#
# Terms
#
class TestTerms(TestCase):

    def testTerm(self):
        term = hchain.XXTerm(3, 4)
        self.assertEqual(term.qubit_index, 3)
        self.assertEqual(term.num_qubits, 4)

    def testXX(self):
        xx = hchain.XXTerm(1, 2)
        self.assertEqual(xx.gate1, gates.X)
        self.assertEqual(xx.gate2, gates.X)

    def testYY(self):
        yy = hchain.YYTerm(4, 8)
        self.assertTrue(np.array_equal(yy.gate1, gates.Y))
        self.assertTrue(np.array_equal(yy.gate2, gates.Y))

    def testZZ(self):
        zz = hchain.ZZTerm(1, 2)
        self.assertEqual(zz.gate1, gates.Z)
        self.assertEqual(zz.gate2, gates.Z)

    def testPairTermMatrix(self):
        xx = hchain.XXTerm(1, 2)
        m = xx.exponential(1j / 2)

        self.assertTrue(np.allclose(x1x2_exp_r2, m, atol=0.0001))

    def testPairTermMatrixWrapAround(self):
        yy = hchain.YYTerm(2, 2)  # Will be Y2Y1
        m = yy.exponential(1j / 10)
        self.assertTrue(np.allclose(y2y1_exp_r10, m, atol=0.0001))

    def testZTerm(self):
        z = hchain.ZTerm(1, 10, 0.1)
        self.assertEqual(1, z.qubit_index)
        self.assertEqual(10, z.num_qubits)
        self.assertEqual(0.1, z.v_coefficient)

    def testZTermMatrix(self):
        v = 0.2
        z = hchain.ZTerm(1, 2, v)
        m = z.exponential(1j / 5)
        self.assertTrue(np.allclose(z1_exp_r5, m, atol=0.0001))



class TestHeisenbergChain(TestCase):

    n = 10
    v = [1.0] * 10

    def setUp(self):
        self.chain = hchain.HeisenbergChain(self.n, self.v)

    def test_init(self):
        self.assertEqual(self.n, self.chain.n)
        self.assertEqual(self.v, self.chain.v)

    def test_str(self):
        desc = self.chain.__str__()
        expected = 'n: 10, v: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]'
        self.assertEqual(expected, desc)

    def test_unitary(self):
        small_chain = hchain.HeisenbergChain(2, [1] * 2)
        actual = small_chain.exponential(1j)
        expected = np.array([[-0.6536-0.7568j, 0.0000+0.0000j,  0.0000+0.0000j, 0.0000+0.0000j],
                             [0.0000+0.0000j,  0.2720+0.5944j, -0.6882+0.3149j, 0.0000+0.0000j],
                             [0.0000+0.0000j, -0.6882+0.3149j,  0.2720+0.5944j, 0.0000+0.0000j],
                             [0.0000+0.0000j,  0.0000+0.0000j,  0.0000+0.0000j, 1.0000+0.0000j]])
        self.assertTrue(np.allclose(actual, expected, atol=0.001))

