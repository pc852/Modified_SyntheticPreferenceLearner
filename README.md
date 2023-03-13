# SyntheticPreferenceGenerator
An extensible python program which generates sets of synthetic preference examples from randomly generated model of specified preference languages.


## Dependencies:

  Pytorch: https://pytorch.org/
  GenCPNet: https://github.com/nmattei/GenCPnet


## Usage:

  `python3 SynthPrefGen.py [options] [config file]`

- Options:
  `-p problem subproblem` specifies the problem and subproblem to run.

  Problem Numbers:

  |Problem Number| Description |
  |--------------|-------------|
  | 1            | Learning Preferences with Neural Networks.|
  | 2            | Learning Preferences with Lexicographic Preference Models.|
  | 3            | Learning Preferences with Simulated Annealing.|
  | 4            | Various related baselines.|

  Subproblem numbers for problems 1-3

  |Subproblem Number| Description |
  |--------------|-------------|
  | 1               | Learning Preferences from a single agent. |
  | 2               | Learning Joint Preferences (Utilitarian).|
  | 3               | Learning Joint Preferences (Maximin).|
  | 4               | Learning Preferences from a single agent (Full Evaluation).|

  Note: Subproblem 3 for problem 1 is not implemented.

  Subproblem for problem 4:

  | Subproblem | Description |
  |--------------|-------------|
  | 1          | Builds and analyzes full fitness graph.|
  | 2          | Builds and analyzes partial fitness graph using hill climbing.|
  | 3          | Analyzes basic hill climbing and random restart approach. |

  `-i [config file]`

  Specifies the type of model to be learned by simulated annealing (default: 113RPF_learn.config).
  Note: Only applies to problems 2 and 4.

  `-l [n]`

  Specifies the number of hidden layers to add to the neural network (default: 3, max: 3).
  Note: Only applies to problem 1.

  `-o [filename]`

  Specifies the name of the data output file (default: a.out).


#Warning
  This software is provided as-is and while efforts have been made to make it more
  user friendly, improper usage may render undesired results.
