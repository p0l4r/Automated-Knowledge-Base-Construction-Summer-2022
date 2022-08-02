#!/usr/bin/env bash
# run_evaluate.sh <input_file> <output_file> <groundtruth_type_file>
# Ex: run_evaluate.sh test.tsv results.tsv test-types.tsv

args="${@:4}"
echo 'Running typing...'
echo "Input file: $1"
echo "Output file: $2"
python run.py $1 $2
echo 'Finish typing!'
echo 'Evaluating the output ...'
echo "Groundtruth type file: $3"
python evaluate.py $2 $3
