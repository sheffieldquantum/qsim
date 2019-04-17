#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

import matplotlib

matplotlib.rcParams['font.family'] = 'serif'

EXP_12_RESULTS_FILE = "../../results/exp12/exp12_results.csv"
EXP_13_RESULTS_FILE = "../../results/exp13/exp13_results.csv"

GRAPH_FILE = "../../results/exp11/exp9_vs_exp11_plot.pdf"

exp12_df = pd.read_csv(EXP_12_RESULTS_FILE, delimiter=',').loc[14:]
exp13_df = pd.read_csv(EXP_13_RESULTS_FILE, delimiter=',').loc[13:]

ax = exp12_df.plot(x='n', y='%', marker='.', linewidth=2)
ax.set_ylabel('% of Suzuki Error',  fontsize=18)
ax.set_xlabel('n', fontsize=18)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

exp13_df.plot(ax=ax, x='n', y='%', marker='.', linewidth=2)

ax.legend(['t=10', 't=2n'], fontsize=16)

plt.ylim([0,100])

plt.show()
#plt.savefig(GRAPH_FILE)