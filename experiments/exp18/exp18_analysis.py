import pandas as pd
import os


import hchain
import approx

import matplotlib.pyplot as plt

import matplotlib

import seaborn as sns
import numpy as np

matplotlib.rcParams['font.family'] = 'serif'

def produce_graphs(file_path):

    gen_df = pd.read_csv(os.path.join(file_path, 'general', 'gen_results.csv'))
    gen_df['Type of Sampling'] = 'General'
    suz_df = pd.read_csv(os.path.join(file_path, 'suzuki', 'suz_results.csv'))
    suz_df['Type of Sampling'] = 'Around Suzuki'

    combined_df = pd.concat([gen_df,suz_df]).loc[lambda d: d['r'] == 125]

    suz_mean = np.mean(combined_df['suzuki error'])

    plt.axhline(suz_mean, color='indigo', linewidth=3, label='Average Suzuki Error')

    ax = sns.barplot(x=combined_df['scale'], y=combined_df['sampled error'], hue=combined_df['Type of Sampling'])
    plt.yscale(value='log')

    plt.xlabel('Scale',  fontsize=16)
    plt.ylabel('Sampled Error',  fontsize=16)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14)



    plt.show()


if __name__ == '__main__':
    path = os.path.join('..','..','results','exp18')
    produce_graphs(path)
