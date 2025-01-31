#!/bin/bash

TIME=100

tools=("pdr" "bcar" "fcar" "ic3")
res_files=("record_pdr.txt" "record_bcar.txt" "record_fcar.txt" "record_ic3.txt")
dirs=("pdr-feedback" "backward-car-feedback" "forward-car-feedback" "ic3ref-feedback")

cd ./tool-compare/aigen
chmod +x run.sh
for ((i=0;i<${#tools[@]};i++))
do
	timeout $TIME ./run.sh ${tools[i]}
	cp result/* ../../RQ1_result/compare/aigen
	echo ${tools[i]}
	sleep 1
done

cd ../aigfuzz
chmod +x run.sh
for ((i=0;i<${#tools[@]};i++))
do
        timeout $TIME ./run.sh ${tools[i]}
        cp result/* ../../RQ1_result/compare/aigfuzz
        echo ${tools[i]}
        sleep 1
done

cd ../aigrow-no-feedback
chmod +x run.sh
for ((i=0;i<${#tools[@]};i++))
do
        timeout $TIME ./run.sh ${tools[i]}
        cp result/* ../../RQ1_result/compare/aigrow_no_feedback
        echo ${tools[i]}
        sleep 1
done

cd ../aigrow-single-thread
for ((i=0; i<${#dirs[@]}; i++))
do
        cd ${dirs[i]}
        chmod +x run.sh
        timeout $TIME ./run.sh &> /dev/null
        cp result_thread/record.txt ../../../RQ1_result/compare/aigrow/${res_files[i]}
        echo ${dirs[i]}
        sleep 1
        cd ..
done

cd ../../RQ1_result
python3 plot2.py


