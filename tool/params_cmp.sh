#!/bin/bash

TIME=100

params=("15 70 15" "25 50 25" "20 40 40" "40 40 20")
res_files=("15-70-15.txt" "25-50-25.txt" "20-40-40.txt" "40-40-20.txt")
dirs=("pdr-feedback" "backward-car-feedback" "forward-car-feedback" "ic3ref-feedback")
res_path=("abc-pdr" "backward_car" "forward_car" "ic3-ref")


for ((j=0; j<${#dirs[@]}; j++))
do
	mkdir RQ1_result/${res_path[j]}
	cd ${dirs[j]}
	chmod +x run.sh
	for ((i=0; i<${#params[@]}; i++))
	do
		echo ${params[i]} > params
		timeout $TIME ./run.sh &> /dev/null
		cp result_thread/record.txt ../RQ1_result/${res_path[j]}/${res_files[i]}
		echo ${res_path[j]} ${res_files[i]}
		sleep 1
	done
	cd ..
done

cd RQ1_result
python3 plot.py
