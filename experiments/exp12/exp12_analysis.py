import pandas as pd
import os

import seaborn as sns

import hchain
import approx

import matplotlib

import matplotlib.pyplot as plt


def produce_graphs(file_path):

    matplotlib.rcParams['font.family'] = 'serif'

    df = pd.read_csv(os.path.join(file_path, 'exp12_results.csv')).loc[:6,]
    df = df.drop(['row', 'exp', 'k', 'r', 't'], axis=1)
    df = df.drop(['v_%d'%i for i in range(1,12)], axis=1)
    df = df.drop(['p_%d'%i for i in range(1,6)], axis=1)
    plt.plot(df['n'], df['%'], marker='o', linewidth=2.5, label='Suzuki')
    plt.ylim([0, 100])

    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    path = os.path.join('..','..','results','exp12')
    produce_graphs(path)
