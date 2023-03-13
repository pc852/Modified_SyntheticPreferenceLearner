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
# config_ary='learn'

for config in $config_ary
do
  rm timing.dat
  OUTFILE=$config\_results_LPM
  echo $config.config
  echo $OUTFILE.zip
  python3 wrapper.py -o $OUTFILE.csv $config.config
  zip $OUTFILE.zip $OUTFILE.csv $config.config timing.dat
done
# python3 wrapper.py -o five_227RPF.config_results_113RPF.csv
