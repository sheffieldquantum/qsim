from abc import ABCMeta, abstractmethod
from scipy.linalg import expm
import numpy as np

import settings
import gates

from gates import X, Y, Z

from cachetools import cached, LFUCache
cache_size = 0
if settings.enable_cache():
    cache_size = 500

cache = LFUCache(maxsize=cache_size)


class ChainTerm(metaclass=ABCMeta):

    def __init__(self, qubit_index, num_qubits):
        self.qubit_index = qubit_index
        self.num_qubits = num_qubits

    @cached(cache)
    def exponential(self, coefficient):
        """
        Returns the exponential of the matrix, multiplied by a coefficient
        """

        try:
            coeff = complex(coefficient)
        except ValueError:
            print('coeff type:' + str(type(coefficient)))
            print('coeff value: ' + str(coefficient))

        return expm(coeff*self.matrix())

    @abstractmethod
    def matrix(self):
        pass

    def commutes_with(self, other_term):
        return not (len(set.intersection(self.qubit_indices, other_term.qubit_indices)) != 0
                    and self.name != other_term.name)

    def __hash__(self):
        return str(self).__hash__()


class PairTerm(ChainTerm, metaclass=ABCMeta):

    def __init__(self, qubit_index, num_qubits):
        self.qubit_indices = {qubit_index, qubit_index % num_qubits + 1}
        super().__init__(qubit_index, num_qubits)

    @cached(cache)
    def matrix(self):

        qubit_1, qubit_2 = sorted(list(self.qubit_indices))
        first = gates.op_for_qubit(self.gate1, qubit_1, self.num_qubits)
        second = gates.op_for_qubit(self.gate2, qubit_2, self.num_qubits)
        product = np.matmul(first, second)
        return product

    @cached(cache)
    def exponential(self, coefficient):
        """
        For terms such as e^{X_1X_2}, we can calculate this via direct exponentiation or via the formula
        e^{X_1*X_2} = e^{X * X} * I ... * I ( * =kronecker product). This second approach is more efficient, and
        we use it were possible.
         """
        try:
            coeff = complex(coefficient)
        except ValueError:
            print('coeff type:' + str(type(coefficient)))
            print('coeff value: ' + str(coefficient))

        exp_term = expm(coeff*np.kron(self.gate1.matrix, self.gate2.matrix))

        if self.qubit_index == self.num_qubits:  # wrap around case
            return super().exponential(coeff)
        else:
            res = exp_term if self.qubit_index == 1 else np.eye(2)
            for i in range(2, self.num_qubits):
                if i == self.qubit_index:
                    res = np.kron(res, exp_term)
                else:
                    res = np.kron(res, np.eye(2))
        return res

    def __eq__(self, other):
        return type(self) == type(other) \
           and self.qubit_index == other.qubit_index \
           and self.num_qubits == other.num_qubits

    def __str__(self):
        return self.name + '_' + str(self.qubit_index) + '_' + str(self.qubit_index % self.num_qubits+1)

    def __hash__(self):
        return super().__hash__()


class XXTerm(PairTerm):
    gate1 = X
    gate2 = X
    name = 'X'


class YYTerm(PairTerm):
    gate1 = Y
    gate2 = Y
    name = 'Y'


class ZZTerm(PairTerm):
    gate1 = Z
    gate2 = Z
    name = 'Z'


class ZTerm(ChainTerm):

    name = 'Z'

    def __init__(self, qubit_index, num_qubits, v_coefficient):
        self.qubit_indices = {qubit_index}
        self.v_coefficient = float(v_coefficient)
        super().__init__(qubit_index, num_qubits)

    @cached(cache)
    def matrix(self):
        gate = gates.op_for_qubit(gates.Z, self.qubit_index, self.num_qubits)
        gate_times_v = self.v_coefficient * gate
        return gate_times_v

    @cached(cache)
    def exponential(self, coefficient):
        try:
            coeff = complex(coefficient)
        except ValueError:
            print('coeff type:' + str(type(coefficient)))
            print('coeff value: ' + str(coefficient))

        exp_term = expm(coeff*self.v_coefficient * gates.Z.matrix)

        res = exp_term if self.qubit_index == 1 else np.eye(2)
        for i in range(2, self.num_qubits+1):
            if i == self.qubit_index:
                res = np.kron(res, exp_term)
            else:
                res = np.kron(res, np.eye(2))
        return res

    def __eq__(self, other):
        return type(other) == ZTerm \
           and self.qubit_index == other.qubit_index \
           and self.num_qubits == other.num_qubits   \
           and self.v_coefficient == other.v_coefficient

    def __str__(self):
        return 'v' + self.name + '_' + str(self.qubit_index)

    def __hash__(self):
        return (str(self) + str(self.v_coefficient)).__hash__()
