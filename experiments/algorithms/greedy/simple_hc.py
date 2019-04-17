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
gens = 1000
num_p_values = 5
step_size = 1e-5 #1e-7


def ternary(number, num_digits):
    """ Product a ternary representation of a number, containing num_digits"""
    result = [0] * num_digits
    quotient = number

    if quotient == 0:
        return result

    position = 1

    while quotient > 0:
        quotient, remainder = divmod(quotient, 3)
        result[-position] = remainder
        position += 1

    return result


def greedy():
    """ Run greedy hillclimber. Enumerate neighbourhood and choose best. """
    chain = hchain.HeisenbergChain(num_qubits, v)

    steps = [-step_size, 0, step_size]

    neighbourhood_size = len(steps)**num_p_values

    suzuki = np.array(approx.suzuki(k))
    suzuki_error = approx.error(chain, approx.r_copies(suzuki, r), t)
    print('Suzuki error: {}'.format(suzuki_error))

    # Start at Suzuki
    current = suzuki
    current_error = suzuki_error

    # Start at 1/p_length
    # current = np.array([0.2] * 5)
    # current_error = approx.error(chain, approx.r_copies(current, r), t)

    # Start at suzuki permutation
    # import random
    # random.seed(1234)
    # suzuki_coeff = approx.suzuki(k)
    # random.shuffle(suzuki_coeff)
    # current = np.array(suzuki_coeff)
    # current_error = approx.error(chain, approx.r_copies(current, r), t)

    for gen in range(1, gens+1):

        current_error_percent = 100 * (current_error / suzuki_error)
        print('Gen: {} Best: {} Percent: {} '.format(gen, current_error, current_error_percent))

        all_neighbours = list(range(1, neighbourhood_size))
        random.shuffle(all_neighbours
                       )
        for neighbour_index in all_neighbours:

            move = [step_size * (coeff - 1) for coeff in ternary(neighbour_index, num_p_values)]

            neighbour = current + move

            neighbour_err = approx.error(chain, approx.r_copies(neighbour, r), t)

            neighbour_err_percent = 100 * (neighbour_err / suzuki_error)

            print('Step {} Neighbour {}/{} error: {}, error %: {}'.format(gen, neighbour_index, neighbourhood_size,
                                                                          neighbour_err, neighbour_err_percent))
            if neighbour_err < current_error:
                current = neighbour
                current_error = neighbour_err
                current_error_percent = 100 * (current_error / suzuki_error)
                print('New best: error: {} percent: {} solution: {})'.format(current_error, current_error_percent,
                                                                             current))
                break


if __name__ == '__main__':
    greedy()

