@echo off
chcp 65001

set datafile=data/ER_DataCuration_1.csv
@rem set datafile=data/SMC_5000-6100.csv
@rem set datafile=data/tag.SMC_DataCuration_All.csv

set ymd1="\\b((19|20)\\d{2})\\D+(0?[1-9]|1[012])\\D+(3[01]|[12]\\d|0?[1-9])\\b"

@echo on
python fns/grep.py %ymd1:\\=\% "%datafile%"
