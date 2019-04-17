import os
import sys
import pandas as pd
import numpy as np


def gen_params(lambda_file, row_id, seed, n_values,params_name):

    lam_df = pd.read_csv(lambda_file)

    k = int(lam_df.loc[row_id,'k'])
    r = int(lam_df.loc[row_id,'r'])

    lam = list(lam_df.loc[row_id,'lambda_1':'lambda_%d'%(r*5**(k-1))])

    max_n = max(n_values)

    cols = ['n'] + ['v_%d'%i for i in range(1,max_n+1)] + ['k', 'r'] + ['lambda_%d'%i for i in range(1,len(lam)+1)]
    params_df = pd.DataFrame(columns=cols)
    np.random.seed(seed)

    for n in n_values:
        params_df.loc[len(params_df)+1] = [n] + list(np.random.uniform(-1,1,n)) + \
                                        ['-' for _ in range(n, max_n)] + [k,r] + lam

    exp_folder_name = 'exp9'

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
        lambda_file= sys.argv[1]
        row_id = int(sys.argv[2])-1
        params_name = sys.argv[3]

        gen_params(lambda_file=lambda_file,
                   row_id=row_id,
                   seed = 324,
                   n_values = range(4,11),
                   params_name = params_name)