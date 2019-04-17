import pandas as pd
import os

import seaborn as sns

import hchain
import approx

import matplotlib

import matplotlib.pyplot as plt


def produce_graphs(file_path):

    matplotlib.rcParams['font.family'] = 'serif'

    df = pd.read_csv(os.path.join(file_path, 'exp5_results_sorted.csv'))

    ax = sns.boxplot(df['r'], list(map(lambda x: 100-x, list(df['% error']))), color='royalblue')
    ax.set_ylim([0,100])
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=18, ticks=[0,1],labels=['r=25','r=50'])
    ax.set_xlabel('')
    ax.set_ylabel('% Error Reduction',  fontsize=18)

    plt.show()


if __name__ == '__main__':
    path = os.path.join('..','..','results','exp5')
    produce_graphs(path)
