import pandas as pd
import os

import math

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

import hchain
import approx

matplotlib.rcParams['font.family'] = 'serif'

def plot(folder_path):
    df = pd.read_csv(os.path.join(folder_path, 'exp16_results.csv'))

    v = list(df.loc[0,'v_1':'v_5'])
    chain= hchain.HeisenbergChain(5,v)
    suz_errs = [approx.error(chain,approx.suzuki_solution(2,r),10) for r in range(25,401,25)]
    r_counts = range(25,401,25)



    for i in range(0,len(df),16):
        df_r = df.loc[i:i+15]
        orig_r = int(df_r.loc[i,'original_r'])
        plt.plot(r_counts,df_r['error'], color=(1.0,1- orig_r/400 ,1- orig_r/400,0.8),
                            marker='.', linewidth=1.5, markersize=4, label='_nolegend_')


    plt.plot(r_counts,suz_errs, color='blue', marker='.', linewidth=2, markersize=7, label = 'Suzuki')
    plt.yscale(value='log')

    plt.legend(fontsize=16)

    plt.xlabel('r',  fontsize=18)
    plt.ylabel('Absolute Error',  fontsize=18)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)


    plt.show()

if __name__ == '__main__':
    path = os.path.join('..','..','results','exp16')
    #add_column(path)
    plot(path)
