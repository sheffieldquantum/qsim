import numpy as np
import os

from exp_util.generate_parameters import gen_params

if __name__ == '__main__':

    np.random.seed(31038752)
    n = 5

    v_vals = [np.random.uniform(-1, 1, n) for _ in range(5)]
    k_vals = [2]
    r_vals = [75, 125]
    seed_vals = [460591, 768387, 948039, 1115242, 1187090, 1552725,
                 1813704, 2259964, 2422921, 3488656, 3648721,
                 3679669, 3901933, 5560785, 5692317, 6016665,
                 6335549, 6387322, 7588418, 7822578, 7913248,
                 8597652, 8805269, 8996026, 9001963, 9555957,
                 9809859, 9869527, 9926156, 9962042]

    gen_vals = [250]

    exp_folder_name = 'exp3'

    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp3_path = os.path.join(results_path, exp_folder_name)
    if not os.path.isdir(exp3_path):
        os.makedirs(exp3_path)

    output_file = os.path.join(exp3_path, 'params.csv')

    gen_params(n=n,
               v_values=v_vals,
               k_values=k_vals,
               r_values=r_vals,
               seed_values=seed_vals,
               gen_values=gen_vals,
               algorithm='CMAES',
               kind='p',
               output_file=output_file)
