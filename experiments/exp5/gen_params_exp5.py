import numpy as np
import os

from exp_util.generate_parameters import gen_params

if __name__ == '__main__':

    np.random.seed(31038752)
    n = 5

    v_vals = [np.random.uniform(-1, 1, n) for _ in range(12)]
    k_vals = [3]
    r_vals = [25, 50]
    seed_vals = [678261680, 951689995, 164252281]
    gen_vals = [500]

    exp_folder_name = 'exp5'

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

    output_file = os.path.join(exp1_path,'params.csv')

    gen_params(n=n,
               v_values=v_vals,
               k_values=k_vals,
               r_values=r_vals,
               seed_values=seed_vals,
               gen_values=gen_vals,
               algorithm='CMAES',
               kind='p concatenated',
               output_file=output_file)
