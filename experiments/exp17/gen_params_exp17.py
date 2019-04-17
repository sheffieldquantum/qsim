import argparse
import random
import csv

EXP_ID = '17'

R_VALUE = 125
NUM_PROBS = 3
TIME_VALS = [1, 5, 9, 13, 17]
OUTPUT_FILE = './exp' + str(EXP_ID) + '_params'
OUTPUT_HEADER = ['exp', 'row', 'n', 'k', 'r', 't', 'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'orig_error', 'orig_suzuki_error']


def read_all(csvfile):
    rows = []
    with open(csvfile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows


def gen_params(exp7_file1, exp7_file2, exp7_file3):

    for exp7_file in [exp7_file1, exp7_file2, exp7_file3]:

        rows = read_all(exp7_file)

        param_file = OUTPUT_FILE + '_r' + rows[0]['r'] + '.csv'

        with open(param_file, 'w') as outcsv:

            lambda_headings = [k for k in rows[0].keys() if k.startswith('lambda_')]

            writer = csv.DictWriter(outcsv, OUTPUT_HEADER + lambda_headings)
            writer.writeheader()

            out_row_id = 1

            for row in rows:

                v_vect = {k: v for k, v in row.items() if k.startswith('v_')}
                lambda_vect = {k: l for k, l in row.items() if k.startswith('lambda_')}

                out_row = {'exp': EXP_ID, 'row': out_row_id, 'n': row['n'], 'k': row['k'], 'r': row['r'],
                           'orig_error': row['optimised error'], 'orig_suzuki_error': row['suzuki error']}

                out_row.update(lambda_vect)
                out_row.update(v_vect)

                for sim_time in TIME_VALS:

                    out_row['t'] = str(sim_time)
                    out_row['row'] = out_row_id

                    writer.writerow(out_row)

                    out_row_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate parameters for Experiment ' + EXP_ID)
    parser.add_argument('exp7_output1', type=str, )
    parser.add_argument('exp7_output2', type=str, )
    parser.add_argument('exp7_output3', type=str, )
    args = parser.parse_args()
    gen_params(args.exp7_output1, args.exp7_output2, args.exp7_output3)