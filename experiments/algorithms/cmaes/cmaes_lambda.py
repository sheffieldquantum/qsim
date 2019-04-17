import hchain
import approx

import os
import numpy as np
import pandas as pd
import time
import random
import util

from deap import base
from deap import creator
from deap import tools
from deap import cma

from deap import algorithms

NORMALISE = False
norm_f = util.mult_norm

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def run_cmaes_lambda(v, k, r, seed, generations, sig=None):

    suzuki = approx.suzuki_solution(k,r)

    if sig == None:
        sig = 1e-5 / len(suzuki)

    chain = hchain.HeisenbergChain(len(v), v)

    random.seed(seed)
    np.random.seed(seed)

    # Error from target
    def target_error(ind):
        if NORMALISE:
            norm_ind = norm_f(ind)
        else:
            norm_ind = ind

        return approx.error(chain, ind, t=2 * chain.n),

    toolbox = base.Toolbox()
    toolbox.register("evaluate", target_error)

    strategy = cma.Strategy(centroid=suzuki, sigma=sig)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaGenerateUpdate(toolbox, ngen=generations, stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof
