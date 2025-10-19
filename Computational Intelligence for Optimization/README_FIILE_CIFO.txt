In this file, we summarise the content of all the folders and subsequent files that our delivery contains.

The work was divided the following way:

Corssino Tchavana Nº 20220597  -  Grid-Search Set-Up
Eduardo Palma Nº 20221022 - Visualizations
Miguel Ramos Nº 20210581 - Representation, Fitness Function, Statistical Analysis
José Matos Nº 20220607 - Selection, Crossover, and Mutation Methods

The "easy_first_grid_search.zip", "easy_parameter_tuning.zip", "hard_first_grid_search.zip", "hard_parameter_tuning.zip" have to be UNZIPPED FIRST.


The report is the file "CIFO_Report_Group_13.pdf"

- "charles.py" includes the implementation of the Individual and Population classes. The Population class includes the "store" method that enables us to save the results from our grid-search executions in .csv files.

- "selection.py" contains the implementation of the selection methods we adapted to our problem and subsequently implemented.

- "mutation.py" contains the implementation of the mutation methods we adapted to our problem and subsequently implemented.

- "crossover.py" contains the implementation of the crossover methods we adapted to our problem and subsequently implemented.

- "scheduling_problem.py" is the file where we implement the best algorithm based on our findings in the "Statistical Analysis.ipynb".The file can run the both difficulty levels versions of the problem.To switch between difficulty levels, the imports from both data sheets are ready, it is only needed to uncomment one of the import lines and comment the other.

- "data_easy.py" is the file where we provide the relevant data for the easy difficulty version of our problem

- "data_medium_hard.py" is the file where we provide the relevant data for the medium-hard difficulty version of our problem

- "grid_search_combinations.py" is the file where we search for the best combination of crossover mutation and selection methods. Each combination was executed for 35 times with 100 generations each. The fitness value of each generation of each run is stored in a .csv file in the "easy_first_grid_search" and "hard_first_grid_search" folders(depending on the difficulty level of the problem we are searching parameters for) and subsequent test folder. The name of each file is a combination of the names of each method being used(crossover, mutation and selection, respectively). To switch between difficulty levels, the imports from both data sheets are ready, it is only needed to uncomment one of the import lines and comment the other.

- "grid_search_parameter_tuning.py" is the file where we search for the best values for mutation and crossover probablities for the best model found on the previous file. We also combine all these possibilities with two possible mutation methods("binary_mutation" and "swap_mutation") as these had very similar average fitness results when used in combination with the best combination of the crossover and selection methods. Each combination was executed for 35 times with 100 generations each. The fitness value of each generation of each run is stored in a .csv file in the "easy_parameter_tuning" and "hard_parameter_tuning" folders(depending on the difficulty level of the problem we are searching parameters for) and subsequent test folder. The name of each file is a combination of both the probabilities being used and reference to each of the best two mutation methods we used. To swith between difficulty levels, the imports from both data sheets are ready, it is only needed to uncomment one of the import lines and comment the other.

- "Statistical Analysis.ipynb" is the Jupyter Notebook where we performed the statistical analysis of the fitness values stored in the "easy_first_grid_search", "hard_first_grid_search", "easy_parameter_tuning" and "hard_parameter_tuning" folders to select our best algorithm.