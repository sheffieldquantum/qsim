import pandas as pd

import approx, hchain
import sys, os


def compare_lambda_over_n(input_filename, input_df, start_row, end_row, output_folder_path):
    df = input_df.copy()
    df.insert(1,'optimised error', None)
    df.insert(1,'suzuki error', None)
    df.insert(1,'%', None)
    if not os.path.isdir(output_folder_path):
        os.makedirs(output_folder_path)

    input_filename_prefix = os.path.splitext(input_filename)[0]
    output_data_path = os.path.join(output_folder_path, input_filename_prefix + '_output_{}_{}.csv'.format(start_row, end_row))

    for row_id in range(start_row - 1, end_row):
        row = df.loc[row_id]

        n = int(row['n'])
        v = list(map(float, list(row['v_1':'v_%d' % n])))
        k = int(row['k'])
        r = int(row['r'])

        lam = list(row.loc['lambda_1':'lambda_%d' % (r * 5 ** (k - 1))])
        chain = hchain.HeisenbergChain(n, v)

        suz_err = approx.error(chain, approx.suzuki_solution(k, r), t=2 * n)
        op_err = approx.error(chain, lam, t=2 * n)

        perc = 100 * op_err / suz_err

        df.loc[row_id,'suzuki error'] = suz_err
        df.loc[row_id,'optimised error'] = op_err
        df.loc[row_id,'%'] = perc

    df.dropna(inplace=True)
    df.to_csv(output_data_path, index=False)

if __name__ == '__main__':

    input_df = pd.read_csv(sys.argv[1])
    start_row = int(sys.argv[2])
    end_row = int(sys.argv[3])

    input_filename = os.path.basename(sys.argv[1])

    exp_folder_name = 'exp9'

    results_path =os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp_path = os.path.join(results_path, exp_folder_name)

    compare_lambda_over_n(input_filename, input_df=input_df,
                  start_row=start_row,
                  end_row=end_row,
                  output_folder_path=exp_path)


