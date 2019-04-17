import pandas as pd
import os
import numpy as np

import seaborn as sns

import matplotlib

import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'serif'

def produce_graphs(path):

    fig, ax= plt.subplots()
    for i in range(31, 61):

        df = pd.read_csv(os.path.join(path, 'logs', 'row_%d.csv'%i))

        ax.plot(list(df['gen']), list(df['min']))

        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        #formatter=matplotlib.ticker.ScalarFormatter(useMathText=True, useOffset=True)
        #ax.yaxis.set_major_formatter(formatter)
        ax.set_yticklabels(["{:.1e}".format(t) for t in ax.get_yticks()])
        ax.set_xlabel('Generations',  fontsize=16)
        ax.set_ylabel('Absolute Error',  fontsize=16)

   #plt.savefig(os.path.join(path, 'plot.jpeg'), dpi=300)

    plt.tight_layout()

    plt.show()


def produce_boxplots(path):

    df = pd.read_csv(os.path.join(path, 'exp3_results_sorted.csv'))
    df['% Error Reduction'] = list(map(lambda x: 100-x, list(df['% error'])))


    prob1_df = pd.DataFrame(df.loc[30:59])
    prob1_df['problem'] = 'Problem 1'
    prob2_df = pd.DataFrame(df.loc[90:119])
    prob2_df['problem'] = 'Problem 2'
    prob3_df = pd.DataFrame(df.loc[150:179])
    prob3_df['problem'] = 'Problem 3'


    print('prob1 median: ' + str(np.median(prob1_df['% Error Reduction'])))
    print('prob2 median: ' + str(np.median(prob2_df['% Error Reduction'])))
    print('prob3 median: ' + str(np.median(prob3_df['% Error Reduction'])))

    print('prob1 range: ' + str(np.ptp(prob1_df['% Error Reduction'])))
    print('prob2 range: ' + str(np.ptp(prob2_df['% Error Reduction'])))
    print('prob3 range: ' + str(np.ptp(prob3_df['% Error Reduction'])))


    combined_df = pd.concat([prob1_df, prob2_df, prob3_df])
    ax = sns.boxplot(y=combined_df['% Error Reduction'], x=combined_df['problem'])
    plt.ylim([1,100])

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)
    plt.ylabel('% Error Reduction', fontsize=16)
    plt.xlabel('')

    plt.tight_layout()

    plt.show()




if __name__ == '__main__':
    path = os.path.join('..', '..', 'results', 'exp3')
    produce_graphs(path)
    #produce_boxplots(path)
