import os
import sys
import pandas as pd
import numpy as np


def gen_params(p_file, row_id, seed, n_values,params_name):

    p_df = pd.read_csv(p_file)

    k = int(p_df.loc[row_id,'k'])
    r = int(p_df.loc[row_id,'r'])

    p = list(p_df.loc[row_id,'p_1':'p_%d'%(5**(k-1))])

    max_n = max(n_values)

    cols = ['n'] + ['v_%d'%i for i in range(1,max_n+1)] + ['k', 'r'] + ['p_%d'%i for i in range(1,len(p)+1)]
    params_df = pd.DataFrame(columns=cols)
    np.random.seed(seed)

    for n in n_values:
        params_df.loc[len(params_df)+1] = [n] + list(np.random.uniform(-1,1,n)) + \
                                        ['-' for _ in range(n, max_n)] + [k, r] + p

    exp_folder_name = 'exp10'

    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..','..', '..', 'results')

    exp1_path = os.path.join(results_path, exp_folder_name)
    if not os.path.isdir(exp1_path):
        os.makedirs(exp1_path)

    params_df.index.name = 'id'
    params_df.to_csv(os.path.join(exp1_path,params_name))


if __name__ == '__main__':
        p_file= sys.argv[1]
        row_id = int(sys.argv[2])-1
        params_name = sys.argv[3]

        gen_params(p_file=p_file,
                   row_id=row_id,
                   seed = 324,
                   n_values = range(4,7),
                   params_name = params_name)