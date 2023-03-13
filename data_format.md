# Data Output Format
----

## Data Pills CSV Format
----

All data generated from this problem is output according to a simple CSV-style
file format in plain text.

Each line of a Data Pills file consists of multiple "pills". A pill consists of
a some number of entries, typically numeric in nature, which are separated by
semicolons and surrounded in parentheses, with each pill being separated by a
comma.

For example if a program generates three data points per run and a run generates
the numbers 0.4, 0.5, and 0.1 then the resulting pill would be `(0.4;0.5;0.1)`.


Since each line contains multiple pills and each pill represents the data
gathered from a single run each line of a Data Pills file has its first pill set
to be a label pill. Label pills follow the same format as a normal data pill, but
it is not meant to be analyzed the same as a data pill.

While it general use of the Data Pills CSV format does not require that each pill
be of the same dimension, we adhere to this practice as a matter of practicality
to simplify our data processing.


## Data Labels
----

Below we provide an ordered list of each data pill for each type of data run.

1. Learning a single preference representation:

   1. Training Accuracy (proportion of correctly decided examples.)
   2. Validation Accuracy (proportion of correctly decided examples.)
   3. Proportion of example set labeled with strict dispreference (<)
   4. Proportion of example set labeled with dispreference (<=)
   5. Proportion of example set labeled with equally preferred (=)
   6. Proportion of example set labeled with preference (>=)
   7. Proportion of example set labeled with strict preference (>)
   8. Proportion of example set labeled with incomparablility (||)

2. Learning a joint preference model:

   1. Training Accuracy for each agent (proportion of correctly decided examples, as many entries as agents.)
   2. Validation Accuracy for each agent (proportion of correctly decided examples, as many entries as agents.)

3. Fitness space analysis:

   1. Number of maxima (or number of attempts in the case of a Monte Carlo).
   2. Evaluation score of the maxima with the worst evaluation.
   3. Average evaluation score of a maxima.
   4. Evaluation score of the global maximum (or best maxima in the case of a Monte Carlo).

4. When comparing a learned NN model to the full preference model:

  1. Training Accuracy (proportion of correctly decided examples.)
  2. Validation Accuracy (proportion of correctly decided examples.)
  3. Full Accuracy proportion of correctly decided examples compared against the original agent.)
  4. Cyclicity (proportion of alternatives which dominate themselves.)

4. When comparing a SA learned RPF to the full preference model:

  1. Training Accuracy (proportion of correctly decided examples.)
  2. Validation Accuracy (proportion of correctly decided examples.)
  3. Full Accuracy proportion of correctly decided examples compared against the original agent.)
