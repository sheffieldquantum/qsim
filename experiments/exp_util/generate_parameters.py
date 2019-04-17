import pandas as pd


def gen_params(n, v_values, k_values, r_values, seed_values, gen_values, algorithm, kind, output_file):

    """
    This writes a csv to the specified output_file location, where each row is a possible combination of parameters.

    :param algorithm:       refers to algorithm used (only for reference) eg. CMAES, 1+1
    :param kind:            refers to which vector is evolved eg. lambda, p, p expanded, 2p ... (only for reference)
    :param output_file:     string of output file, should include .csv extension

    """

    cols = ['n'] + ['v_%d'%i for i in range(1,n+1)] + ['k', 'r', 'seed', 'gens', 'algorithm', 'kind']

    df = pd.DataFrame(columns=cols)

    for v in v_values:
        assert(len(v)==n)
        for k in k_values:
            for r in r_values:
                for seed in seed_values:
                    for gen in gen_values:
                        df.loc[len(df)+1] = [n] + list(v) + [k, r, seed, gen, algorithm, kind]

    df.index.name = 'id'
    df.to_csv(output_file)


