import argparse
import random
import csv

EXP_ID = '14'

R_VALUE = 125
NUM_PROBS = 3
TIME_VALS = [1, 5, 9, 13, 17]
OUTPUT_FILE = './exp' + str(EXP_ID) + '_params.csv'
OUTPUT_HEADER = ['exp', 'row', 'n', 'k', 'r', 't', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'v_1', 'v_2', 'v_3', 'v_4', 'v_5']


def read_all(csvfile):
    rows = []
    with open(csvfile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['r']) == R_VALUE:
                rows.append(row)
                if len(rows) == NUM_PROBS:
                    break
    return rows


def gen_params(exp3_result_file):

    rows = read_all(exp3_result_file)
    out_row_id = 1

    with open(OUTPUT_FILE, 'w') as outcsv:

        writer = csv.DictWriter(outcsv, OUTPUT_HEADER)
        writer.writeheader()

        for row in rows:

            p_vect = {k: v for k, v in row.items() if k.startswith('p_')}
            v_vect = {k: v for k, v in row.items() if k.startswith('v_')}

            for sim_time in TIME_VALS:

                out_row = {'exp': EXP_ID, 'row': out_row_id, 'n': row['n'], 'k': row['k'], 'r': R_VALUE,
                           't': str(sim_time)}

                out_row.update(p_vect)
                out_row.update(v_vect)

                writer.writerow(out_row)

                out_row_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate parameters for Experiment ' + EXP_ID)
    parser.add_argument('exp3_output', type=str, )
    args = parser.parse_args()
    gen_params(args.exp3_output)