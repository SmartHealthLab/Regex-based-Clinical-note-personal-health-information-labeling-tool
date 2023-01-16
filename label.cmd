@echo off
chcp 65001

set findlog=true
set cfg[0]=disease_kcd
set cfg[1]=smc

@echo on
python fns/label.py config/%cfg[0]%.yml config/%cfg[1]%.yml --findlog %findlog%
