from unittest import TestCase


import gates as gates
import numpy as np

x = np.array([[0, 1], [1, 0]])
y = np.array([[0, -1j], [1j, 0]])
z = np.array([[1, 0], [0, -1]])

# Two qubit system
x1_two_qubit = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
x2_two_qubit = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
y1_two_qubit = np.array([[0, 0, -1j, 0], [0, 0, 0, -1j], [1j, 0, 0, 0], [0, 1j, 0, 0]])
y2_two_qubit = np.array([[0, -1j, 0, 0], [1j, 0, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]])

z1_two_qubit = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
z2_two_qubit = np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

# Three qubit system
y2_three_qubit = np.array([[0,  0, -1j,   0,  0,  0,   0,   0],
                           [0,  0,   0, -1j,  0,  0,   0,   0],
                           [1j, 0,   0,   0,  0,  0,   0,   0],
                           [0, 1j,   0,   0,  0,  0,   0,   0],
                           [0,  0,   0,   0,  0,  0, -1j,   0],
                           [0,  0,   0,   0,  0,  0,   0, -1j],
                           [0,  0,   0,   0, 1j,  0,   0,   0],
                           [0,  0,   0,   0,  0, 1j,   0,   0]])

z3_three_qubit = np.array([[1,  0,   0,   0,  0,   0,   0,   0],
                           [0, -1,   0,   0,  0,   0,   0,   0],
                           [0,  0,   1,   0,  0,   0,   0,   0],
                           [0,  0,   0,  -1,  0,   0,   0,   0],
                           [0,  0,   0,   0,  1,   0,   0,   0],
                           [0,  0,   0,   0,  0,  -1,   0,   0],
                           [0,  0,   0,   0,  0,   0,   1,   0],
                           [0,  0,   0,   0,  0,   0,   0,  -1]])


class TestGates(TestCase):

    def test_defs(self):
        self.assertTrue(np.array_equal(x, gates.X.matrix))
        self.assertTrue(np.array_equal(y, gates.Y.matrix))
        self.assertTrue(np.array_equal(z, gates.Z.matrix))

    def test_single_op(self):
        op = gates.op_for_qubit(gates.X, 1, 1)
        self.assertTrue(np.array_equal(gates.X.matrix, op))

    def test_y(self):
        op = gates.op_for_qubit(gates.Y, 2, 2)
        expected = np.array([[ 0, -1j,  0,    0],
                             [1j,   0,  0,    0],
                             [ 0,   0,  0,   -1j],
                             [ 0,   0,  1j,   0]])
        self.assertTrue(np.array_equal(expected, op))

    def test_x1(self):
        op = gates.op_for_qubit(gates.X, 1, 2)
        self.assertTrue(np.array_equal(x1_two_qubit, op))

    def test_x2(self):
        op = gates.op_for_qubit(gates.X, 2, 2)
        self.assertTrue(np.array_equal(x2_two_qubit, op))

    def test_y1(self):
        op = gates.op_for_qubit(gates.Y, 1, 2)
        self.assertTrue(np.array_equal(y1_two_qubit, op))

    def test_y2(self):
        op = gates.op_for_qubit(gates.Y, 2, 2)
        self.assertTrue(np.array_equal(y2_two_qubit, op))

    def test_z1(self):
        op = gates.op_for_qubit(gates.Z, 1, 2)
        self.assertTrue(np.array_equal(z1_two_qubit, op))

    def test_z2(self):
        op = gates.op_for_qubit(gates.Z, 2, 2)
        self.assertTrue(np.array_equal(z2_two_qubit, op))

    def test_y2_three_qubit(self):
        op = gates.op_for_qubit(gates.Y, 2, 3)
        self.assertTrue(np.array_equal(y2_three_qubit, op))

    def test_z3_three_qubit(self):
        op = gates.op_for_qubit(gates.Z, 3, 3)
        self.assertTrue(np.array_equal(z3_three_qubit, op))

    def test_invalid_index(self):
        self.assertRaises(ValueError, gates.op_for_qubit, gates.X, 10, 5)

