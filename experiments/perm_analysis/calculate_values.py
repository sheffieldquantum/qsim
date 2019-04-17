import hchain
import approx
import numpy as np
import pandas as pd

import os


def calc_values():

    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..','..', '..', 'results')

    path = os.path.join(results_path, 'perm_analysis')
    if not os.path.isdir(path):
        os.makedirs(path)

    np.random.seed(1294635)

    n = 5
    chain = hchain.HeisenbergChain(n, np.random.uniform(-1,1,n))

    group_perm = [4 * i for i in range(chain.n)] + [4 * i + 1 for i in range(chain.n)] \
                        + [4 * i + 2 for i in range(chain.n)] + [4 * i + 3 for i in range(chain.n)]

    can_perm = [i for i in range(4*chain.n)]

    rand_perms = [np.random.permutation(4*chain.n) for _ in range(20)]

    cols = ['r', 'gate count', 'error']
    group_k2 = pd.DataFrame(columns=cols)
    group_k3 = pd.DataFrame(columns=cols)

    can_k2 = pd.DataFrame(columns=cols)
    can_k3 = pd.DataFrame(columns=cols)

    rand_k2 = pd.DataFrame(columns=cols)
    rand_k3 = pd.DataFrame(columns=cols)


    k=2
    for r in range(25,401,25):
        print(r)
        suz = approx.suzuki_solution(k,r)
        group_k2.loc[len(group_k2)] = [r, approx.gate_count(chain,len(suz),permutation=group_perm),
                                           approx.error(chain,suz,t=2*chain.n, permutation=group_perm)]

        can_k2.loc[len(can_k2)] = [r, approx.gate_count(chain,len(suz),permutation=can_perm),
                                           approx.error(chain,suz,t=2*chain.n, permutation=can_perm)]

        mean_gate_count, mean_error = 0, 0
        for perm in rand_perms:
            mean_gate_count += approx.gate_count(chain, len(suz), permutation=perm)
            mean_error += approx.error(chain, suz,  t=2*chain.n, permutation=perm)

        mean_gate_count = mean_gate_count/len(rand_perms)
        mean_error = mean_error / len(rand_perms)
        rand_k2.loc[len(rand_k2)] = [r, mean_gate_count, mean_error]

    group_k2.to_csv(os.path.join(path,'Grouped k=2.csv'))
    can_k2.to_csv(os.path.join(path, 'Canonical k=2.csv'))
    rand_k2.to_csv(os.path.join(path, 'Random k=2.csv'))



    k=3
    for r in range(5,61,5):
        print(r)
        suz = approx.suzuki_solution(k, r)
        group_k3.loc[len(group_k3)] = [r, approx.gate_count(chain,len(suz), permutation=group_perm),
                                           approx.error(chain, suz, t=2*chain.n, permutation=group_perm)]

        can_k3.loc[len(can_k3)] = [r, approx.gate_count(chain, len(suz), permutation=can_perm),
                                           approx.error(chain, suz, t=2*chain.n, permutation=can_perm)]

        mean_gate_count, mean_error = 0, 0
        for perm in rand_perms:
            mean_gate_count += approx.gate_count(chain, len(suz), permutation=perm)
            mean_error += approx.error(chain, suz, t=2 * chain.n, permutation=perm)

        mean_gate_count = mean_gate_count / len(rand_perms)
        mean_error = mean_error / len(rand_perms)
        rand_k3.loc[len(rand_k3)] = [r, mean_gate_count, mean_error]

    group_k3.to_csv(os.path.join(path, 'Grouped k=3.csv'))
    can_k3.to_csv(os.path.join(path, 'Canonical k=3.csv'))
    rand_k3.to_csv(os.path.join(path, 'Random k=3.csv'))

    df = pd.DataFrame(columns=['n'] + ['v_%d' % i for i in range(1, chain.n+1)])
    df.loc[len(df)] = [chain.n] + list(chain.v)

    df.to_csv(os.path.join(path, 'chain.csv'))


if __name__ == '__main__':
    calc_values()




