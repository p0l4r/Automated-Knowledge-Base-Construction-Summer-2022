#!/bin/bash

echo "OPEN INFORMATION EXTRACTION"

INPUTFILE=./oie_corpus/sentences.txt
OUTFILE=./results.txt
RESFILE=./pr_result.dat
GTFILE=./oie_corpus/extractions-groundtruth.oie

echo "Input: ${INPUTFILE}"
echo "Output: ${OUTFILE}"

python run.py $INPUTFILE $OUTFILE

echo "The results, saving in ... ${RESFILE}"

python benchmark.py --gold=$GTFILE --out=$RESFILE --clausie=$OUTFILE

echo "DONE! The result is saved ${RESFILE}."