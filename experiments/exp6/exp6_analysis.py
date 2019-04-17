import pandas as pd
import os

import seaborn as sns

import hchain
import approx

import matplotlib.pyplot as plt

import matplotlib

matplotlib.rcParams['font.family'] = 'serif'

def produce_graphs(file_path):

    df = pd.DataFrame()

    n4_df = pd.read_csv(os.path.join(file_path, 'n=4', 'exp6_n4_results_sorted.csv'))
    df['n=4'] = list(map(lambda x: 100-x, list(n4_df['% error'])))

    n6_df = pd.read_csv(os.path.join(file_path, 'n=6', 'exp6_n6_results_sorted.csv'))
    df['n=6'] = list(map(lambda x: 100-x, list(n6_df['% error'])))

    n7_df = pd.read_csv(os.path.join(file_path, 'n=7', 'exp6_n7_results_sorted.csv'))
    df['n=7'] = list(map(lambda x: 100-x, list(n7_df['% error'])))


    ax = sns.violinplot(data=df,)
    ax.set_ylim([0,100])
    ax.set_ylabel('% Error Reduction', fontsize=18)
    plt.xticks( fontsize=18)
    plt.yticks(fontsize=16)

    plt.tight_layout()

    plt.show()




if __name__ == '__main__':
    path = os.path.join('..','..','results','exp6')
    produce_graphs(path)
