import numpy as np
import os

from exp_util.generate_parameters import gen_params

if __name__ == '__main__':

    np.random.seed(31038752)
    n = 6

    v_vals = [np.random.uniform(-1, 1, n) for _ in range(3)]
    k_vals = [2]
    r_vals = [100]
    seed_vals = [699911460, 300619650, 768199526]
    gen_vals = [250]

    exp_folder_name = os.path.join('exp6', 'n=6')

    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp1_path = os.path.join(results_path, exp_folder_name)
    if not os.path.isdir(exp1_path):
        os.makedirs(exp1_path)

    output_file = os.path.join(exp1_path, 'params_n6.csv')

    gen_params(n=n,
               v_values=v_vals,
               k_values=k_vals,
               r_values=r_vals,
               seed_values=seed_vals,
               gen_values=gen_vals,
               algorithm='CMAES',
               kind='p',
               output_file=output_file)
