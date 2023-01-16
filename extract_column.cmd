
@echo off
chcp 65001 > NUL

set datafile=data/ER_DataCuration_1.csv
@rem set datafile=data/SMC_5000-6100.csv
@rem set datafile=data/tag.SMC_DataCuration_All.csv

set rowperfile=1000
set column=현병력-Free Text#13
set outfile=data/column/%column:#=_%.txt

@echo on
python fns/column2txt.py -c "%column%" -n %rowperfile% -i "%datafile%" -o "%outfile%"
