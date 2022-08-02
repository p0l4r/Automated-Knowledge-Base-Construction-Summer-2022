#!/usr/bin/env bash
# run_evaluate.sh <results.csv>
# Ex: run_evaluate.sh

INPUT='input.csv'
GT='groundtruth.csv'
RESULT='results.csv'
echo 'Running extraction...'
echo "Input file: $INPUT"
echo "Output file: $RESULT"
python run.py $INPUT $RESULT
echo 'Finish labeling!'
echo 'Evaluating the output ...'
echo "Groundtruth type file: $GT"
python evaluate.py $RESULT $GT
