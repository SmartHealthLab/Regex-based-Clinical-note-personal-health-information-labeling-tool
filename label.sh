#!/bin/bash

# grep -E "\s[0-9]{2}\.[1-9]\s" *.txt

# python fns/label.py smc_find --findlog true 2>&1 | tee -a logs/deid.label.smc.log
# status=${PIPESTATUS}
# if [ ${status[0]} -ne 0 ]; then
#     echo "exit code: ${status[0]}"
#     exit ${status[0]}
# fi
# exit 0

python fns/label.py config/disease_kcd.yml config/smc.yml --findlog false 2>&1 | tee -a logs/label.smc.log
status=${PIPESTATUS}
if [ ${status[0]} -ne 0 ]; then
    echo "exit code: ${status[0]}"
    exit ${status[0]}
fi
# exit 0

# DROOT=/home/timecandy/data/삼성병원.스마트큐레이션
# FILES=( \
#     "환자내원사유-Text#6" \
#     "주증상-Text#7" \
#     "부증상-Text#11" \
#     "주호소-Free Text#12" \
#     "현병력-Free Text#13" \
#     "과거력-Free Text#14" \
#     "산과력 - Free text#16" \
#     "가족력-Free Text#17" \
#     "개인력 및 사회력-Free Text#18" \
#     "계통문진-Free Text#19" \
#     "신체검진-Free Text#20" \
#     "본원-Text#25" \
#     "외부-Text#26" \
#     "문제목록-Free Text#27" \
#     "임상진단명 자동완성검색기능#29" \
#     "진단명-Free Text#30" \
# )

# for ii in ${!FILES[*]}
# # for ii in 1
# do
#     cnt=-1
#     if [ $ii -eq 1 ]; then
#         cnt=1000
#     fi

#     cfname="${FILES[$ii]//#/_}"

#     for entry in "${DROOT}/r_freetext/${cfname}".*.txt
#     do
#         dir=${entry%/*}
#         fname=${entry##*/}
#         cp "$entry" "${dir}/b_${fname}"
#         # mv "$entry" "${dir}/c_${fname}"
#     done

#     # tagfile="${DROOT}/tag.SMC_5000-6100.csv"
#     tagfile="${DROOT}/tag.SMC_DataCuration_All.csv"
#     python fns/column2txt.py \
#         -i "${tagfile}" \
#         -c "${FILES[$ii]}" \
#         -n ${cnt} \
#         -o "${DROOT}/r_freetext/${cfname}.txt" \
#         2>&1 | tee -a logs/column2txt.label.log

#     # for entry in "${DROOT}/r_freetext/${cfname}".*.txt
#     # do
#     #     dir=${entry%/*}
#     #     fname=${entry##*/}
#     #     stem=${fname%.*}
#     #     ext=${fname##*.}

#     #     python fns/compare.py "${dir}/b_${fname}" "$entry" 2>&1 | tee -a logs/compare.b.log
#     #     # cp "${dir}/diff_b_${stem}.html" /mnt/c/Users/timec/Downloads/
#     #     ls "${dir}/diff_b_${stem}.html"

#     #     python fns/compare.py "${dir}/c_${fname}" "$entry" 2>&1 | tee -a logs/compare.c.log
#     #     # cp "${dir}/diff_c_${stem}.html" /mnt/c/Users/timec/Downloads/
#     #     ls "${dir}/diff_c_${stem}.html"
#     # done
# done
