#!/bin/bash

#change me
EXE_DIR="/media/ginochacon/gino/physical_machine_measurements/"

# ${1} --> number of pages allocated
# ${2} --> number of iterations
# ${3} --> when THP is off use 4kb, when THP is on use mix_page_sizes ---> if you don't like it find another way to differentiate between THP on/off

${EXE_DIR}/a.out ${1} ${2} &
bash collect_stats.sh $! ${1} ${2} ${3}


