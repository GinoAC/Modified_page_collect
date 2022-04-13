#!/bin/bash

#change it
OUT_DIR="/media/ginochacon/gino/physical_machine_measurements/Statistics"
EXE_DIR="/media/ginochacon/gino/physical_machine_measurements/page-collect/"
         
echo "Begin Collect Stats"
echo 1 ${1} 2 ${2} 3 ${3} 4 ${4}

#periodically call page-collect and grab the statistics to check the usage of 2MB pages as the benchmark executes
while [ -n ${1} -a -d "/proc/${1}" ]; do
		echo "running pagecollect"
    sleep 1
    sudo ${EXE_DIR}page-collect -p ${1} -o ${OUT_DIR}/pagecollect_${2}_${3}_${4}.txt # make sure that the stats are appended in the output file
done
