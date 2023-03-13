#!/bin/bash
# MIN=$1
# MAX=$2
# CONFIG=$3
#
# for i in `seq $MIN $MAX`
# do
#   NEWFILE=$CONFIG\_results_$i\L_256
#   rm timing.dat
#   python3 wrapper.py -l $i -o $NEWFILE.csv $CONFIG
#   zip $NEWFILE.zip $NEWFILE.csv $CONFIG timing.dat
# done

config_ary='baseline_multi five_113RPF five_227RPF five_CPNet_0 five_CPNet_7'
single_config_ary='learn_min'

for config in $single_config_ary
do
  rm timing.dat
  OUTFILE=$config\_results_SA_13311ASO_full
  echo $config.config
  python3 wrapper.py -p 3 4 -i 13311ASO_learn.config -o $OUTFILE.csv $config.config
  zip $OUTFILE.zip $OUTFILE.csv $config.config timing.dat
done

# for config in $config_ary
# do
#   rm timing.dat
#   OUTFILE=$config\_results_SA_33722ASO_util
#   echo $config.config
#   python3 wrapper.py -p 3 2 -i 33722ASO_learn.config -o $OUTFILE.csv $config.config
#   zip $OUTFILE.zip $OUTFILE.csv $config.config timing.dat
# done
#
# for config in $config_ary
# do
#   rm timing.dat
#   OUTFILE=$config\_results_SA_33722ASO_mm
#   echo $config.config
#   python3 wrapper.py -p 3 3 -i 33722ASO_learn.config -o $OUTFILE.csv $config.config
#   zip $OUTFILE.zip $OUTFILE.csv $config.config timing.dat
# done

# python3 wrapper.py -o five_227RPF.config_results_113RPF.csv
