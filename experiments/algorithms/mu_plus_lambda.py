import approx
import numpy as np

import random
import array

import hchain

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


def run_es(v, k, r, suz, seed, gens, mu=1, lambd=1, step_size=None, indpb=0.2):

    chain = hchain.HeisenbergChain(len(v),v)

    random.seed(seed)
    np.random.seed(seed)

    if step_size is None:
        step_size = 5e-5/len(suz)
        print(len(suz))

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, typecode="d", fitness=creator.FitnessMin, strategy=None)
    creator.create("Strategy", array.array, typecode="d")

    def generateES(icls, scls, step):
        ind = icls(suz)
        ind.strategy = scls(step*(-1)**np.random.randint(0, 2) for _ in range(len(suz)))
        return ind

    def target_error(ind):
        final_ind = approx.r_copies(ind,int((r*5**(k-1))/len(ind)))

        return approx.error(chain, final_ind, t=2*chain.n),

    toolbox = base.Toolbox()
    toolbox.register("individual", generateES, creator.Individual, creator.Strategy, step_size)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxESBlend, alpha=0.1)
    toolbox.register("mutate", tools.mutESLogNormal, c=1.0, indpb=indpb)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate",  target_error)

    pop = toolbox.population(n=mu)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, logbook = algorithms.eaMuPlusLambda(population=pop, toolbox=toolbox, mu=mu, lambda_=lambd,
                                              cxpb=0, mutpb=1, ngen=gens, stats=stats, halloffame=hof)

    return pop, logbook, hof
