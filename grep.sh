#!/bin/bash

logfile=./logs/grep.log
rm -f ${logfile}

ymd1="\\b((19|20)\\d{2})\\D+(0?[1-9]|1[012])\\D+(3[01]|[12]\\d|0?[1-9])\\b"
datafile="~/data/ER_DataCuration_1.csv"

python fns/grep.py "${ymd1}" "${datafile}" 2>&1 | tee -a ${logfile}
exit 0

# tag0=PERIOD_YMDKHMP2KHMP
# tag1=PERIOD_YMDKHMP2KHP
# tag2=PERIOD_YMDKHP2KHP
# tag3=PERIOD_MDKHP2MDKHP
# tag4=PERIOD_MDKHP2KHP
# tag5=PERIOD_KHMP2KHMP
# tag6=PERIOD_KHMP2KHP
# tag7=PERIOD_KHKP2KHP
# tag8=PERIOD_KHP2KHMP
# tag9=PERIOD_KHP2KHKP
# tag10=PERIOD_KHP2KHP
# tag11=PERIOD_YMD2YMD
# tag12=PERIOD_YMD2MD
# tag13=PERIOD_YMD2D
# tag14=PERIOD_MD2MD
# tag15=PERIOD_MD2D
# tag16=PERIOD_D2D
# tag17=DATETIME_YMDKHMP
# tag18=DATETIME_YMDKHKP
# tag19=DATETIME_YMDKHP
# tag20=DATETIME_MDKHMP
# tag21=DATETIME_MDKHKP
# tag22=DATETIME_MDKHP
# tag23=DATETIME_DKHP
# tag24=DATE_YMD
# tag25=DATE_MDY
# tag26=DATE_MD
# tag27=DATE_YM
# tag28=DATE_D
# tag29=TIME_KHMP
# tag30=TIME_KHKP
# tag31=TIME_KHP

# rm -f ./logs/grep.log
# for ii in {0..31}; do
#     tag="tag${ii}"
#     python fns/grep.py "<${!tag}>[^<]+</${!tag}>" "${datafile}" 2>&1 | tee -a ${logfile}
# done
# exit 0