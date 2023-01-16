#!/bin/bash

filename=현병력.01.txt
stem=${filename%.*}

logfile=./logs/compare.${filename%.*}.log
rm -f ${logfile}

python fns/compare.py "data/tag/${filename}" "data/org/${filename}" 2>&1 | tee -a ${logfile}
