# Quantum-Simulation-Optimisation
Approximating a Heisenberg Chain with Trotter-Suzuki decompositions.

The core source code is in the _qsim_ directory, with tests in _test_.

Experiments are in _experiments_, with a readme containing summaries of each experiment.

Parameter files are split across _results_ and _experiments_.

Results files are in csv format and are in _results_. Often these files had to be recombined and sorted to be ran on a HPC cluster.

### Example
To create an instance of a HeisenbergChain:

```
import numpy as np
import hchain

n = 5 # number of qubits/system size
v = np.random.uniform(n)

chain = hchain.HeisenbergChain(n=n,v=v)
``` 

Then to get the error of a particular Trotter-Suzuki Decomposition (specified by _k_ and _r_):

```
import approx

k = 2
r = 100
lambda_vector = approx.suzuki_solution(k,r)

t = 2 * chain.n  # we simulate for time proportional to system size

error = approx.error(chain=chain, lambda_v=lambda_vector, t=t)
```
