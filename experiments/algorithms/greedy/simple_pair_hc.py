import numpy as np
import hchain
import approx
import random

# Taken from first line of cmaes/problems.csv
num_qubits = 5
v = [0.3929383711957233, -0.42772133009924107, -0.5462970928715938, 0.10262953816578246, 0.43893793957112615]
k = 2
r = 106
t = 2 * num_qubits
precalc_suzuki_error = 0.0009927360836838363
gens = 100000
num_p_values = 5
step_size = 1e-5 #1e-7


def greedy():
    """ Run greedy hillclimber. Enumerate neighbourhood and choose best. """

    random.seed(1234)

    chain = hchain.HeisenbergChain(num_qubits, v)

    suzuki = np.array(approx.suzuki(k))
    suzuki_error = approx.error(chain, approx.r_copies(suzuki, r), t)
    print('Suzuki error: {}'.format(suzuki_error))

    # Start at Suzuki
    current = suzuki
    current_error = suzuki_error

    for gen in range(1, gens+1):

        current_error_percent = 100 * (current_error / suzuki_error)
        print('Gen: {} Best: {} Percent: {} '.format(gen, current_error, current_error_percent))

        first = random.randint(1, num_p_values)
        second = random.randint(1, num_p_values)

        neighbour = current.copy()
        neighbour[first-1] = neighbour[first-1] + step_size
        neighbour[second-1] = neighbour[second-1] - step_size

        neighbour_err = approx.error(chain, approx.r_copies(neighbour, r), t)

        neighbour_err_percent = 100 * (neighbour_err / suzuki_error)

        print('Step {}  error: {}, error %: {}'.format(gen, neighbour_err, neighbour_err_percent))

        if neighbour_err < current_error:
            current = neighbour
            current_error = neighbour_err
            current_error_percent = 100 * (current_error / suzuki_error)
            print('New best: error: {} percent: {} solution: {})'.format(current_error, current_error_percent,
                                                                             current))


if __name__ == '__main__':
    greedy()

