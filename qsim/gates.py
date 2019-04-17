import numpy as np
import settings
from cachetools import cached, LFUCache

cache_size = 0
if settings.enable_cache():
    cache_size = 100

cache = LFUCache(maxsize=cache_size)


class Gate:
    pass


class XGate(Gate):
    def __init__(self):
        self.matrix = np.array([[0, 1], [1, 0]])


class YGate(Gate):
    def __init__(self):
        self.matrix = np.array([[0, -1j], [1j, 0]])


class ZGate(Gate):
    def __init__(self):
        self.matrix = np.array([[1, 0], [0, -1]])


# Use these variables, not the classes.
X = XGate()
Y = YGate()
Z = ZGate()


@cached(cache)
def op_for_qubit(gate, index, num_qubits):
    """
    Returns matrix operator representing the given gate applied to the qubit at the given index in an num_qubits system,
    via the kronecker product I * ... * X * ... * I
    """

    if index < 1 or index > num_qubits:
        raise ValueError('Invalid index: ' + str(index))

    if num_qubits < 1:
        raise ValueError('Invalid number of qubits: ' + str(num_qubits))

    if index == 1:
        matrix = gate.matrix
    else:
        matrix = np.eye(2)

    for j in range(2, num_qubits+1):
        if j == index:
            matrix = np.kron(matrix, gate.matrix)
        else:
            matrix = np.kron(matrix, np.eye(2))

    return matrix
