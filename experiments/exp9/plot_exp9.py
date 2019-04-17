#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

RESULTS_FILE = "../../results/exp9/exp9_results.csv"
GRAPH_FILE = "../../results/exp9/exp9_plot.pdf"

df = pd.read_csv(RESULTS_FILE, delimiter=',')

ax = df.plot(x='n', y='%', legend=False, title="Exp9: Generalisation over n and t where t=2n")
ax.set_ylabel('Percentage of Suzuki Error')

plt.savefig(GRAPH_FILE)