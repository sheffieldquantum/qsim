import os
import argparse
import csv

import approx
import hchain

EXP_ID = '17'
OUTPUT_DIR = '../results/exp' + EXP_ID + '/'


def read_all(csvfile):
    rows = []
    with open(csvfile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
        return reader.fieldnames, rows


def run(input_file, start, end):

    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    input_file_prefix = os.path.splitext(os.path.basename(input_file))[0]

    output_file = os.path.join(OUTPUT_DIR, input_file_prefix + '_output_{}_{}.csv'.format(start, end))

    header, all_rows = read_all(input_file)

    with open(output_file, 'w') as outcsv:

        output_header = header + ['suzuki_error', 'error', '%']

        writer = csv.DictWriter(outcsv, output_header)
        writer.writeheader()

        for row in all_rows[start-1:end]:

            print("Processing: " + row['row'])

            n = int(row['n'])
            k = int(row['k'])
            r = int(row['r'])
            t = int(row['t'])

            lambda_vect = {k: l for k, l in row.items() if k.startswith('lambda_') and l != ''}
            lambda_values = [float(l) for l in lambda_vect.values()]

            v_vect = {k: v for k, v in row.items() if k.startswith('v_') and v != ''}
            v_values = [float(v) for v in v_vect.values()]

            chain = hchain.HeisenbergChain(n, v_values)

            suz_err = approx.error(chain, approx.suzuki_solution(k, r), t)
            op_err = approx.error(chain, lambda_values, t)

            percentage = 100 * op_err / suz_err

            row['suzuki_error'] = suz_err
            row['error'] = op_err
            row['%'] = percentage


            writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run generalisation experiments')
    parser.add_argument('inputfile', type=str, )
    parser.add_argument('startline', type=int)
    parser.add_argument('endline', type=int)
    args = parser.parse_args()
    run(args.inputfile, args.startline, args.endline)