import pandas as pd
import os

import math

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

import hchain
import approx

matplotlib.rcParams['font.family'] = 'serif'

def add_column(folder_path):

    df = pd.read_csv(os.path.join(folder_path, 'exp15_results.csv'))

    for i in range(len(df)):
        print(i)

        row = df.loc[i]
        v = list(row['v_1':'v_5'])
        r = int(row['r'])
        k = int(row['k'])
        t = int(row['t'])
        chain = hchain.HeisenbergChain(5,v)

        df.loc[i,'v_suz_error'] = approx.error(chain,approx.suzuki_solution(k,r),t)

        df.to_csv(os.path.join(folder_path,'exp15_results_vcol.csv'))


def plot(folder_path):
    df = pd.read_csv(os.path.join(folder_path, 'exp15_results_vcol.csv'))

    vals = []
    for i in range(len(df)):
        row = df.loc[i]
        if not math.isclose(row['suzuki_error'], row['v_suz_error'], abs_tol=1e-5):
            val =100- 100*row['error']/row['suzuki_error']
            vals.append(val)

    ax= sns.boxplot(vals,orient='v')

    plt.ylim([0, 100])
    plt.ylabel('% Error Reduction',  fontsize=18)
    plt.yticks(fontsize=16)
    plt.show()



if __name__ == '__main__':
    path = os.path.join('..','..','results','exp15')
    #add_column(path)
    plot(path)
