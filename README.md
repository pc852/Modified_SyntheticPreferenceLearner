# Modified SyntheticPreferenceGenerator
A modified version of the SyntheticPreferenceGenerator written by Dr. Michael Huelsman https://github.com/xLeachimx/SyntheticPreferenceLearner. 

### Dependencies
***
Refer to the original version of README for installation instructions. **IMPORTANT**: Before installation of genCPnet package, search in the files "degen_multi.cc", "netcount.cc", and "tables.h" and change the string "factorial" to another string (e.g. factoria). This is because the string "factorial" clashes with content from the dependecy gmp.

### Overview
***
Refer to the orginal version of README for other functionalities. This version further includes generating 100 example pairs with labels from a chosen preference type, and the option to run learning experiments with asprin.


### Usage
*** 
On top of the original commands, a program 5 is newly added for learning with asprin. 
`python3 SynthPrefGen.py -p 5 <subprogram> pref_model.config`
Subprogram details:
|  Subprogram | Description |
|--|--|
| 0 | Generates 100 examples pairs with labels and store them locally in the relative directory "../Asprin/temp\_run"/, and the details of the chosen preference type is stored in "../Asprin/Generated\_Preference\_Model/"|
| 1 | Execute 5-fold cross validation learning with asprin using existing local files in the directory above containing example pairs, outputing training and validation accuracies |
| 2 | Combination of subprograms 0 and 1, in that order |
| 3 | Subprogram 2 executed 25 times |
