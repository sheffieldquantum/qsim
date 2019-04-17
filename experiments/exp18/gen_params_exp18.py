import numpy as np
import os
import pandas as pd


def generate_params():

    np.random.seed(31038752)
    n = 5

    v_vals = [np.random.uniform(-1, 1, n) for _ in range(10)]
    k2_vals = [75, 125]
    k3_vals = [25, 50]
    scale_vals = [10**(-i) for i in range(1, 8, 2)]

    exp_folder_name = 'exp18'

    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp1_path = os.path.join(results_path, exp_folder_name)
    if not os.path.isdir(exp1_path):
        os.makedirs(exp1_path)

    output_file = os.path.join(exp1_path, 'params.csv')

    cols = ['n'] + ['v_%d'%i for i in range(1, n+1)] + ['k', 'r', 'scale']

    df = pd.DataFrame(columns=cols)

    for v in v_vals:


        for k2_val in k2_vals:
            for s in scale_vals:
                df.loc[len(df)+1] = [n] + list(v) + [2, k2_val,s]
        for k3_val in k3_vals:
            for s in scale_vals:
                df.loc[len(df)+1] = [n] + list(v) + [3, k3_val,s]

    df.index.name = 'id'
    df.to_csv(output_file)


if __name__ == '__main__':
    generate_params()
