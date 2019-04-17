import argparse
import csv

EXP_ID = '16'

OUTPUT_FILE = './exp' + str(EXP_ID) + '_params.csv'
OUTPUT_HEADER = ['exp', 'row', 'n', 'k', 'r', 't', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'v_1', 'v_2', 'v_3', 'v_4', 'v_5',
                 'original_error', 'suzuki_error', 'original_r']


def read_all(csvfile):
    rows = []
    with open(csvfile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    # Take first 16 rows, which are the optimisation for a given v over lots of r values.
    first_runs = rows[0:16]
    return first_runs


def gen_params(exp2_results_file):

    # Get 30 problems and their optimised solutions
    rows = read_all(exp2_results_file)

    out_row_id = 1

    with open(OUTPUT_FILE, 'w') as outcsv:

        writer = csv.DictWriter(outcsv, OUTPUT_HEADER)
        writer.writeheader()

        for row in rows:

            out_row = {'exp': EXP_ID, 'row': out_row_id, 'n': row['n'], 'k': row['k'],
                       't': 2*int(row['n']), 'original_error': row['optimised error'], 'suzuki_error': row['suzuki error'],
                       'original_r': row['r']}

            p_vect = {k: v for k, v in row.items() if k.startswith('p_')}
            out_row.update(p_vect)

            v_vect = {k: v for k, v in row.items() if k.startswith('v_')}
            out_row.update(v_vect)

            for row in rows:

                out_row['r'] = row['r']
                out_row['row'] = out_row_id

                writer.writerow(out_row)

                out_row_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate parameters for Experiment ' + EXP_ID)
    parser.add_argument('exp2_output', type=str, )
    args = parser.parse_args()
    gen_params(args.exp2_output)