import matplotlib.pyplot as plt


import pandas as pd

import hchain
import matplotlib

import os


def plot(path):
    matplotlib.rcParams['font.family'] = 'serif'

    line_styles=['solid', 'dashed', 'dotted']*2

    fig, ax = plt.subplots(figsize=(30,20))
    plt.loglog()
    for file_name in os.listdir(path):
        if file_name == 'chain.csv':
            df = pd.read_csv(os.path.join(path, file_name))
            n = int(df.loc[0,'n'])
            v = [round(i, 6) for i in list(df.loc[0,'v_1':'v_%d'%(n+1)])]
            chain = hchain.HeisenbergChain(n,v)
        elif file_name[-4:] =='.csv':
           df =pd.read_csv(os.path.join(path,file_name))
           plt.plot(df['gate count'], df['error'], label=file_name[:-4],
                    linewidth=2, linestyle=line_styles.pop(0), marker='.')



           if 'Grouped k=2' in file_name:
                plt.annotate('k=2', (list(df['gate count'])[0], list(df['error'])[0]), fontsize=18,
                             textcoords='offset pixels', xytext=(30,0))
           elif 'Grouped k=3' in file_name:
                plt.annotate('k=3', (list(df['gate count'])[0], list(df['error'])[0]), fontsize=18,
                             textcoords='offset pixels', xytext=(30,0))






    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.legend(fontsize=20)
    plt.hlines([10 ** (-i) for i in range(0, 6)], xmin=3 * 10 ** 3, xmax=7*10 ** 4, colors='#feb0b2')
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter(useMathText=True))
    ax.set_xticks([5e3,1e4,2e4,5e4])

    ax.set_xticklabels(['5×10$^{3}$','1×10$^{4}$','2×10$^{4}$','5×10$^{4}$'])

    plt.title(str(chain) + ', t: 2n', fontsize=20)
    ax.set_xlabel('Total Gate Count', fontsize=22, labelpad=20)

    ax.set_ylabel('Absolute Error',  fontsize=22)

    #plt.savefig(os.path.join(path, 'perm_plot.png'), dpi=fig.dpi)
    plt.tight_layout()
    plt.gcf().subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

    plt.show()

if __name__ == '__main__':
    results_path = os.path.join('..', 'results')
    if not os.path.isdir(results_path):
        results_path= os.path.join('..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..', '..', 'results')
    if not os.path.isdir(results_path):
        results_path = os.path.join('..','..','..', '..', 'results')

    path = os.path.join(results_path, 'perm_analysis')
    if not os.path.isdir(path):
        os.makedirs(path)

    plot(path)
