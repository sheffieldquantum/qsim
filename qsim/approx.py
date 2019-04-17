import numpy as np
import settings

from cachetools import cached, TTLCache
from cachetools.keys import hashkey
cache_size = 0
if settings.enable_cache():
    cache_size = 100000

cache = TTLCache(maxsize=cache_size, ttl=1000)


def error(chain, lambda_v, t, permutation=None):
    """
    :param chain: A HeisenbergChain object.
    :param lambda_v: A lambda vector.
    :param t: Simulation time, t.
    :param permutation: Optional, permutation of terms relative to 'canonical permutation'

    :return: Norm error between approximation and target unitary e^{-itH}
    """

    if permutation is None:
        # 'Grouped permutation': allows similar terms to be combined
        permutation =[4 * i for i in range(chain.n)] + [4 * i + 1 for i in range(chain.n)] \
                        + [4 * i + 2 for i in range(chain.n)] + [4 * i + 3 for i in range(chain.n)]


    seg = [chain.terms[i] for i in permutation]
    rev_seg = seg[::-1]
    term_list = seg + rev_seg

    matrix = np.eye(2**chain.n)
    for phase in lambda_v:
        matrix = np.matmul(matrix, term_mult(chain.n, phase, t, terms=term_list))

    desired = chain.exponential(-1j * t)

    return np.linalg.norm(desired - matrix, ord=2)


def gate_count(chain, M, permutation=None):
    """
    :param chain: A HeisenbergChain object.
    :param M: Length of the lambda vector, i.e. number of second order decompositions in the product.
    :param permutation: Optional, different permutations allow similar terms to combine and reduce the gate count.
                        Default: 'Grouped permutation'

    :return: Number of exponential gates needed for the above parameters.
    """

    if permutation is None:
        permutation =[4 * i for i in range(chain.n)] + [4 * i +1 for i in range(chain.n)] \
                        + [4 * i +2 for i in range(chain.n)] + [4 * i + 3 for i in range(chain.n)]

    terms = get_terms(chain,permutation,M)
    gate_count = 0

    for term in set(terms):

        gate_count += 1
        indices = []
        for i in range(len(terms)):
            if terms[i] == term:
                indices.append(i)

        for j in range(len(indices)-1):
            if not can_be_brought_together(terms, indices[j], indices[j+1]):
                gate_count += 1

    return gate_count


def get_terms(chain,permutation,M):
    """
    Returns a list of term objects corresponding to a approximation of (lambda vector) length M.
    """
    seg = [chain.terms[i] for i in permutation]
    rev_seg = seg[::-1]
    term_list = (seg + rev_seg)*M
    return term_list


def can_be_brought_together(terms, index_1, index_2):
    """
    Returns True if the terms located and index_1 and index_2 are the same term type and commute with everything
    in between them in the list. Indicates whether we can combine these terms into one term, by combining the
    exponentials.
    """
    t = terms[index_1]

    if t.name != terms[index_2].name:
        return False

    for i in range(index_1, index_2):  # for each term between the indices
        if not t.commutes_with(terms[i]): # does it commute with our term
            return False
    return True


def term_mult_key(*args, terms):
    key = hashkey(args)
    hashed_terms = [hash(term) for term in terms]
    full_key = key + tuple(hashed_terms)
    return full_key



@cached(cache, key=term_mult_key)
def term_mult(n, phase, t, terms):
    result = np.identity(2**n)
    for term in terms:
        result = np.matmul(result, term.exponential(phase / 2 * -1j * t))
    return result


# def npkey(a, b):
#     a.flags.writeable = False
#     b.flags.writeable = False
#     matrix_hash = hash(a.data.tobytes()) + hash(b.data.tobytes())
#     a.flags.writeable = True
#     b.flags.writeable = True
#     return matrix_hash
#
#
# # Added for optimisation
# @cached(cache, key=npkey)
# def mul_prox(a, b):
#     return np.matmul(a,b)

def r_copies(lambda_v, r):
    """Takes a list and concatenates it to itself r times, normalising by dividing by r."""
    return np.array(list(lambda_v) * r) / r


def suzuki(k):
    """Returns an expanded Suzuki lambda vector of 2kth order."""
    assert(k > 0)
    if k == 1:
        return [1]
    else:
        res = []
        p_k = 1 / (4 - 4 ** (1 / (2 * k - 1)))
        for val in [p_k, p_k, 1-4*p_k, p_k, p_k]:
            for t in suzuki(k-1):
                res.append(val*t)
    return res


def suzuki_vals(k_val):
    """Returns an concatenated Suzuki lambda vector of 2 k_val-th order."""
    assert(k_val > 0)
    if k_val == 1:
        return [1]
    else:
        vals = []
        for k in range(k_val, 1, -1):
            p_k = 1 / (4 - 4 ** (1 / (2 * k - 1)))
            vals += [p_k, p_k, 1 - 4 * p_k, p_k, p_k]
        return vals


def expand_vals(vals):
    """Takes a concatenated suzuki vector and expands it out. That is, calling 'suzuki_vals(k)' followed by 'expand_vals'
    should result in 'suzuki(k)'"""
    if len(vals) in [5, 1]:

        return vals
    else:
        assert (len(vals) % 5 == 0)
        exp_vals = []
        split_vals = [vals[i:i + 5] for i in range(0, len(vals), 5)]
        for i in split_vals[0]:
            exp_vals += list(i*np.array(expand_vals(vals[5:])))

        return exp_vals


def suzuki_solution(k, r):
    return r_copies(suzuki(k), r)

