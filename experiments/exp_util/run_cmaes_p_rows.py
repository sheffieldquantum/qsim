import time
import os
import pandas as pd

from algorithms.cmaes.cmaes_p import run_cmaes_p
import approx
import hchain


def evaluate_rows(input_df, start_row, end_row, output_folder_path):
    df = input_df.copy()
    if not os.path.isdir(output_folder_path):
        os.makedirs(output_folder_path)

    logs_path = os.path.join(output_folder_path, 'logs')
    if not os.path.isdir(logs_path):
        os.makedirs(logs_path)

    output_data_path = os.path.join(output_folder_path, 'output_{}_{}.csv'.format(start_row, end_row))

    for row_id in range(start_row-1, end_row):
        row = df.loc[row_id]

        n = int(row['n'])
        v = row['v_1':'v_%d' % n]
        k = int(row['k'])
        r = int(row['r'])
        seed = int(row['seed'])
        gens = int(row['gens'])

        chain = hchain.HeisenbergChain(n, v)

        t = time.time()
        pop, log, hof = run_cmaes_p(v=v, k=k, r=r, seed=seed, generations=gens)
        t = time.time() - t

        best = hof[0]

        suz_err = approx.error(chain,approx.suzuki_solution(k, r),t=2*n)
        op_err = approx.error(chain,approx.r_copies(best, r),t=2*n)
        perc = 100*op_err/suz_err

        for j in range(1,5**(k-1)+1):
            df.loc[row_id,'p_%d'%j] = best[j-1]
        df.loc[row_id,'optimised error'] = op_err
        df.loc[row_id, 'suzuki error'] = suz_err
        df.loc[row_id, '% error'] = perc
        df.loc[row_id, 'time'] = t

        pd.DataFrame(log).to_csv(os.path.join(logs_path, 'row_{}.csv'.format(row_id + 1)), index=False)

    df.dropna(inplace=True)
    df.to_csv(output_data_path, index=False)




