import pandas as pd
import sys
import os

from exp_util.run_cmaes_p_rows import evaluate_rows

if __name__ == '__main__':

    input_df = pd.read_csv(sys.argv[1])
    start_row = int(sys.argv[2])
    end_row = int(sys.argv[3])
    exp_folder_name = 'exp1'

    results_path =os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..', '..', '..', '..', 'results')

    exp_path = os.path.join(results_path, exp_folder_name)

    evaluate_rows(input_df=input_df,
                  start_row=start_row,
                  end_row=end_row,
                  output_folder_path=exp_path)

