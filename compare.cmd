
@echo off
chcp 65001 > NUL

set filename=현병력.01.txt

@echo on
python fns/compare.py "data/tag/%filename%" "data/org/%filename%"
