#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

EXP_9_RESULTS_FILE = "../../results/exp9/exp9_results.csv"
EXP_11_RESULTS_FILE = "../../results/exp11/results.csv"

GRAPH_FILE = "../../results/exp11/exp9_vs_exp11_plot.pdf"

exp9_df = pd.read_csv(EXP_9_RESULTS_FILE, delimiter=',')
exp11_df = pd.read_csv(EXP_11_RESULTS_FILE, delimiter=',')

ax = exp9_df.plot(x='n', y='%', title="Exp9 vs Exp11: Generalisation over n and t")
ax.set_ylabel('Percentage of Suzuki Error')

exp11_df.plot(ax=ax, x='n', y='%')

ax.legend(['t=2n', 't=10'])

# plt.show()
plt.savefig(GRAPH_FILE)