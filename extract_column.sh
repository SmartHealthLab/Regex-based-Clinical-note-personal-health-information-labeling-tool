#!/bin/bash

logfile=logs/column2txt.log
rm -f ${logfile}

DROOT=/home/timecandy/data/삼성병원.스마트큐레이션
FILE_IN= "${DROOT}/ER_DataCuration_1.csv"
COLUMNS=( \
    "주호소-Free Text#12" \
    "현병력-Free Text#13" \
    "과거력-Free Text#14" \
    "위험인자-Free Text#15" \
    "산과력 - Free text#16" \
    "가족력-Free Text#17" \
    "개인력 및 사회력-Free Text#18" \
    "계통문진-Free Text#19" \
    "신체검진-Free Text#20" \
    "정신상태검사(MSE)-Free Text#21" \
    "문제목록-Free Text#27" \
    "전문의 소견-Free Text#28" \
    "임상진단명 자동완성검색기능#29" \
    "진단명-Free Text#30" \
)

for ii in ${!COLUMNS[*]}
# for ii in 1
do
    python fns/column2txt.py \
        -i "${FILE_IN}" \
        -c "${COLUMNS[$ii]}" \
        -n 5000 \
        -o "${DROOT}/out/${COLUMNS[$ii]//#/_}.txt" \
        2>&1 | tee -a logs/column2txt.log
done
