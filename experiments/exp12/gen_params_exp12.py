import argparse
import random
import csv

EXP_ID = '12'

R_VALUE = 125
NUM_PROBS = 3
NUM_QUBITS_VALS = [5, 6, 7, 8, 9, 10, 11]
MIN_QUBITS = min(NUM_QUBITS_VALS)
MAX_QUBITS = max(NUM_QUBITS_VALS)
SIM_TIME = 10
OUTPUT_FILE = './exp' + str(EXP_ID) + '_params.csv'
SEED = -690548112
V_HEADER = ['v_' + str(x) for x in range(1, MAX_QUBITS+1)]
OUTPUT_HEADER = ['exp', 'row', 'n', 'k', 'r', 't', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5'] + V_HEADER


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

    random.seed(SEED)
    rows = read_all(exp3_result_file)
    out_row_id = 1

    with open(OUTPUT_FILE, 'w') as outcsv:

        writer = csv.DictWriter(outcsv, OUTPUT_HEADER)
        writer.writeheader()

        for row in rows:

            p_vect = {k: v for k, v in row.items() if k.startswith('p_')}
            v_vect = {k: v for k, v in row.items() if k.startswith('v_')}

            for num_qubits in NUM_QUBITS_VALS:

                out_row = {'exp': EXP_ID, 'row': out_row_id, 'n': num_qubits, 'k': row['k'], 'r': R_VALUE,
                           't': SIM_TIME}

                out_row.update(p_vect)
                out_row.update(v_vect)

                writer.writerow(out_row)

                v_vect['v_' + str(num_qubits+1)] = random.uniform(0, 2) - 1

                out_row_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate parameters for Experiment ' + EXP_ID)
    parser.add_argument('exp3_output', type=str, )
    args = parser.parse_args()
    gen_params(args.exp3_output)