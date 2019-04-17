#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

RESULTS_FILE = "../../results/exp11/results.csv"
GRAPH_FILE = "../../results/exp11/exp11_plot.pdf"

df = pd.read_csv(RESULTS_FILE, delimiter=',')

ax = df.plot(x='n', y='%', legend=False, title="Exp11: Generalisation over n where t=10")
ax.set_ylabel('Percentage of Suzuki Error')

plt.savefig(GRAPH_FILE)