import pandas as pd
import sys
import os
import numpy as np

import hchain
import approx


def general_sampling(input_df, start_row, end_row, output_folder_path):
    df = input_df.copy()

    NUM_SAMPLES = 100

    for row_id in range(start_row-1, end_row):
        row = df.loc[row_id]

        n = int(row['n'])
        v = row['v_1':'v_%d' % n]
        k = int(row['k'])
        r = int(row['r'])
        scale = float(row['scale'])

        cols = ['n'] + ['v_%d' % i for i in range(1, n+1)] + ['k', 'r', 'scale', 'sampled error', 'suzuki error']

        row_df = pd.DataFrame(columns=cols)

        chain = hchain.HeisenbergChain(n, v)
        sample_length = (5**(k-1))

        for _ in range(NUM_SAMPLES):
            sample_vector = np.random.normal(loc=1/sample_length, scale=scale/sample_length, size=sample_length)
            sampled_err = approx.error(chain, approx.r_copies(sample_vector, r), t=2*n)
            suz_err = approx.error(chain, approx.suzuki_solution(k, r), t=2*n)


            row_df.loc[len(row_df)+1] = [n] + list(v) + [k, r, scale, sampled_err, suz_err]

        row_df.to_csv(os.path.join(output_folder_path,'row_%d.csv'%(row_id+1)))



if __name__ == '__main__':


    input_df = pd.read_csv(sys.argv[1])
    start_row = int(sys.argv[2])
    end_row = int(sys.argv[3])
    exp_folder_name = os.path.join('exp18','general')



    results_path =os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp_path = os.path.join(results_path, exp_folder_name)

    if not os.path.isdir(exp_path):
        os.makedirs(exp_path)

    general_sampling(input_df=input_df,
                     start_row=start_row,
                     end_row=end_row,
                     output_folder_path=exp_path)



