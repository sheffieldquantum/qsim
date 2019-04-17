# Experiments 

All the experiments aim to roughly follow the same structure. For each experiment there is usually:
 
* A module to generate parameters, which except for exp 9 and 10 should stand alone (no inputs). 
* A module to run the experiment, which takes in the input file, the start row and end row to calculate.
The module will then deposit the output rows in the appropriate results directory. 
* An analysis module, to process and visualise the data. 


The parameter files all aim to have the same structure, containing the following as column headings:
 
* n 
* v_1 to v_n 
* k 
* r 
* seed (to get reproducible results for a given run)
* generations 
* algorithm (eg. CMAES, 1+1) 
* kind (eg. lambda vector, p vector, p concatenated) 


The idea is that an experiment can just evaluate a row, by reading off all the relevant information, and outputting
to a similar file with appended columns, such as the optimised vector values, % improvement, and time taken. The log files
for the runs are put in a logs directory in the appropriate results directory.



## Experiment 1 
This experiment aims to consider the spread of error and improvement over different v values. 

This is used to generate Figure 4 in the paper.

The parameters are:



* n = 5
* k = 2 
* 30 v values 
* 4 r values 
* 3 runs (seed) 
* CMAES on the p vector 
* 250 generations 


## Experiment 2  
This experiment aims to consider the spread of error and improvement over different r values.
 
This is used to generate Figure 5 in the paper.
 
The parameters are:

* n = 5
* k = 2 
* 3 v values 
* 16 r values 
* 1 run (seed) 
* CMAES on the p vector 
* 250 generations 


## Experiment 3  
This experiment aims to consider the spread of error and improvement over different runs. The parameters are:

This is used to generate Figures 2 and 3 in the paper.

* n = 5
* k = 2 
* 5 v values 
* 2 r values 
* 30 runs (seed) 
* CMAES on the p vector 
* 250 generations 


## Experiment 4  
This experiment looks at k = 3, applying CMAES to the expanded p vector. The parameters are:

* n = 5
* k = 3 
* 3 v values 
* 2 r values 
* 3 runs (seed) 
* CMAES on the expanded p vector 
* 250 generations 


## Experiment 5  
This experiment looks at k = 3, applying CMAES to the concatenated p vector. 

This is used to generate Figure 7 in the paper.

The parameters are:

* n = 5
* k = 3 
* 3 v values 
* 2 r values 
* 3 runs (seed) 
* CMAES on the concatenated p vector 
* 500 generations 


## Experiment 6  
This experiment considers the case n = 4,6,7. 

This is used to generate Figure 6 in the paper.

The parameters are:

* n = 4,6,7 
* k = 2 
* 3 v values 
* 3 r values 
* 1 run (seed) 
* CMAES on the p vector 
* 250 generations 



## Experiment 7  
This experiment looks at applying 1+1 hill climbing to the full lambda vector. The parameters are:

* n = 5
* k = 2 
* 3 v values 
* 3 r values 
* 1 run (seed) 
* 1+1 on the lambda vector 
* 250 generations 


## Experiment 8  
This experiment looks at applying CMAES to the full lambda vector. The parameters are:

* n = 5
* k = 2 
* 3 v values 
* 1 r value 
* 1 run (seed) 
* CMAES on the lambda vector 
* 200 generations 


## Experiment 9  
This experiment aims to compare an optimised lambda vector against different n values.

gen_params_exp9.py takes as parameters:

* The path to the file containing the optimised lambda vector.
* The row at which the optimised lambda vector is located. 
* The name for the output file (without directories). 


run_exp9.py takes as parameters:

* The input parameters file. 
* The start row. 
* The end row. 


## Experiment 10  
This experiment aims to compare an optimised p vector against different n values.

gen_params_exp10.py takes as parameters:

* The path to the file containing the optimised p vector.
* The row at which the optimised p vector is located. 
* The name for the output file (without directories). 


run_exp10.py takes as parameters:

* The input parameters file. 
* The start row. 
* The end row. 


## Experiment 11 

A repeat of experiment 9 but with constant t=10 instead of t=2n.

Resarch Question: do optimised solutions generalise over n if t is constant?

gen_params_exp9.py takes as parameters:

* The path to the file containing the optimised lambda vector.
* The row at which the optimised lambda vector is located. 
* The name for the output file (without directories). 


run_exp9.py takes as parameters:

* The input parameters file. 
* The start row. 
* The end row. 


## Experiment 12

Generalisation over n with fixed t=10

This is used (with Exp 13) to generate Figure 8 in the paper.

* Uses results of Exp 3 (Robustness over runs on p vector)
* Selects results where R=125, and then selects first three runs
* Tests n=5..11
* t=10
* For new v in v vector, randomly generates values
* Parameter file from Exp3 was not sorted before input, so may be easier just to use our exp12 param

## Experiment 13

This is used (with Exp 12) to generate Figure 8 in the paper.

* Uses results of Exp 3 in same way as Exp 12.
* Same as Exp 12 except t=2n
* Parameter file from Exp3 was not sorted before input, so may be easier just to use our exp13 param

## Experiment 14

Generalisation over t with fixed n=5

* Uses Exp 3 in the same way was Exp 12 and 13
* Parameter file from Exp3 was sorted, so creating parameter file should be replicable.

## Experiment 15

This is used to generate Figure 9 in the paper.

* Generalisation over unseen v.
* Takes results from Exp 1 and filters on r=100
* Takes first of the three reps on each problem.
* Runs each p-vector on all the v vectors found in the file

## Experiment 16

This is used to generate Figure 10 in the paper.

* Generalisation over r
* Uses results from Exp 2.
* Takes first 16 rows from exp 2, Optimisation for a given v over lots of r values.
* Run those results over the other r values in those 16 rows.

## Experiment 17

ES Lambda generalisation over t

## Experiment 18

Sampling. This is used to generate Figure 1 in the paper.

## Perm Analysis

This is used to generate Figure 1 in the appendices.