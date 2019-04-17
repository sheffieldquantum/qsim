import pandas as pd
import os
import seaborn as sns

import matplotlib.pyplot as plt

import matplotlib


def produce_boxplots(file_path):

    matplotlib.rcParams['font.family'] = 'serif'

    df = pd.read_csv(os.path.join(file_path,'exp1_results_sorted.csv'))

    ax = sns.boxplot(x=df['r'], y=list(map(lambda x: 100-x, list(df['% error']))), color='green')
    ax.set_ylim([1, 100])
    ax.set_xlabel('r', fontsize=16)
    ax.set_ylabel('% Error Reduction', fontsize=16)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    #ax.set_title('Improvement over 30 v values', weight='bold', fontsize=15)
    plt.tight_layout()

    #plt.savefig(os.path.join(file_path, 'v_boxplots.pdf'), dpi=600)
    plt.show()


if __name__ == '__main__':
    path = os.path.join('..', '..', 'results','exp1')
    produce_boxplots(path)