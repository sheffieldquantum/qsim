import pandas as pd
import os


import hchain
import approx

import matplotlib.pyplot as plt

import matplotlib


def produce_graphs(file_path):

    matplotlib.rcParams['font.family'] = 'serif'

    df = pd.read_csv(os.path.join(file_path, 'exp2_results_sorted.csv')).loc[lambda d: d['id']>32]

    fig, ax = plt.subplots(figsize=(30,20))
    plt.loglog()

    gate_counts = []

    chain = hchain.HeisenbergChain(5,[1]*5)

    for index, row in df.iterrows():
        k = int(row['k'])
        r = int(row['r'])

        gc= approx.gate_count(chain,r * 5 ** (k - 1))
        gate_counts.append(gc)
        plt.vlines(x=gc, ymin=row['optimised error'], ymax=row['suzuki error'], linestyle=':')

        if r in [25,100,200,300,400]:
            plt.annotate('r=%d'%r, (approx.gate_count(chain, r * 5 ** (k - 1)), row['suzuki error']),
                         textcoords='offset pixels', xytext=(-10,10), fontsize=13)

    plt.plot(gate_counts,df['suzuki error'], marker='o', linewidth=2.5,  label='Suzuki')
    plt.plot(gate_counts, df['optimised error'], marker='o',linewidth=2.5, label='Optimised')
    plt.hlines([10 ** (-i) for i in range(1, 6)], xmin=3 * 10 ** 3, xmax=5 * 10 ** 4, colors='#feb0b2')
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
    ax.set_xticks([5e3,1e4,2e4,5e4])
    ax.set_xticklabels(['5×10$^{3}$','1×10$^{4}$','2×10$^{4}$','5×10$^{4}$'])


    plt.legend(fontsize=20)
    plt.xlabel('Total Gate Count', fontsize=18,labelpad=10)
    plt.ylabel('Absolute Error', fontsize=18)

    #plt.savefig(os.path.join(file_path, 'plots_r.png'), dpi=fig.dpi)
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()





if __name__ == '__main__':
    path = os.path.join('..','..','results','exp2')
    produce_graphs(path)
