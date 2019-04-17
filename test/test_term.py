import numpy as np
from unittest import TestCase

from gates import X,Y,Z
from term import PairTerm, XXTerm,YYTerm,ZZTerm,ZTerm
from scipy.linalg import expm


class MockPairTerm(PairTerm):
    gate1 = np.eye(2)
    gate2 = np.eye(2)
    name = 'Mock'


class TestPairTerm(TestCase):

    def test_init(self):

        M = MockPairTerm(2,6)
        self.assertEqual(6, M.num_qubits)
        self.assertEqual(2, M.qubit_index)
        self.assertEqual({2,3}, M.qubit_indices)

        M = MockPairTerm(10,10)
        self.assertEqual(10, M.num_qubits)
        self.assertEqual(10, M.qubit_index)
        self.assertEqual({10,1}, M.qubit_indices)


class TestXXTerm(TestCase):

    def test_matrix(self):
        xx = XXTerm(2, 6)
        expected = np.kron(np.eye(2),np.kron(X.matrix,np.kron(X.matrix, \
                            np.kron(np.eye(2),np.kron(np.eye(2),np.eye(2))))))

        self.assertTrue(np.allclose(xx.matrix(),expected))

    def test_exp(self):
        for n in [4, 6, 8]:
            for t in [1, 2,-3]:
                for i in [1, int(n/2), n]:
                    xx = XXTerm(i, n)
                    method_1 = xx.exponential(1j*t)
                    method_2 = expm(xx.matrix()*t*1j)

                    self.assertTrue(np.allclose(method_1, method_2))


class TestYYTerm(TestCase):

    def test_matrix(self):
        yy = YYTerm(1,4)
        expected = np.kron(Y.matrix,np.kron(Y.matrix,np.kron(np.eye(2), np.eye(2))))

        self.assertTrue(np.allclose(yy.matrix(), expected))

    def test_exp(self):
        n = 10
        for i in [1, int(n/2), n]:
            yy = YYTerm(i, n)
            method_1 = yy.exponential(2j)
            method_2 = expm(yy.matrix()*2j)

            self.assertTrue(np.allclose(method_1,method_2))


class TestZZTerm(TestCase):

    def test_matrix(self):
        zz = ZZTerm(8,8)
        expected = np.kron(Z.matrix, np.kron(np.eye(2), np.kron(np.eye(2),
                            np.kron(np.eye(2), np.kron(np.eye(2), np.kron(np.eye(2),
                                    np.kron(np.eye(2), Z.matrix)))))))

        self.assertTrue(np.allclose(zz.matrix(), expected))

    def test_exp(self):
        n = 5
        for i in [1, int(n/2), n]:
            zz = ZZTerm(i, n)
            method_1 = zz.exponential(0.5j)
            method_2 = expm(zz.matrix()*0.5j)

            self.assertTrue(np.allclose(method_1,method_2))


class TestZTerm(TestCase):

    def test_matrix(self):
        z = ZTerm(4,5,0.2)
        expected = np.kron(np.eye(2), np.kron(np.eye(2),
                            np.kron(np.eye(2), np.kron(Z.matrix*0.2, np.eye(2)))))

        self.assertTrue(np.allclose(z.matrix(), expected))

    def test_exp(self):
        n = 7
        for i in [1, int(n/2), n]:
            z = ZTerm(i, n, -0.8)
            method_1 = z.exponential(0.5j)
            method_2 = expm(z.matrix()*0.5j)

            self.assertTrue(np.allclose(method_1,method_2))
