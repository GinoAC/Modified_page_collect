#!/bin/bash

# ${1} --> number of pages allocated
# ${2} --> number of iterations

#-e dtlb_load_misses.walk_duration,dtlb_store_misses.walk_duration \
#-e cpu_clk_unhalted.thread_p \

# note that some of the following events (-e) might not be supported by a given microarchitecure since the < perf list > is different across different microarchitecures
perf stat -d -d -e dtlb_load_misses.walk_completed,dtlb_load_misses.walk_completed_4k,dtlb_load_misses.walk_completed_2m_4m,dtlb_load_misses.walk_completed_1g \
	  -e dTLB-loads,dTLB-load-misses,dtlb_load_misses.stlb_hit,dtlb_load_misses.stlb_hit_4k,dtlb_load_misses.stlb_hit_2m,dtlb_load_misses.miss_causes_a_walk\
	  -e dtlb_store_misses.walk_completed,dtlb_store_misses.walk_completed_4k,dtlb_store_misses.walk_completed_2m_4m,dtlb_store_misses.walk_completed_1g \
	  -e inst_retired.any_p \
	  -e itlb_misses.walk_completed,itlb_misses.walk_completed_4k,itlb_misses.walk_completed_2m_4m,itlb_misses.walk_completed_1g,itlb_misses.walk_duration \
	  -e page_walker_loads.dtlb_l1,page_walker_loads.dtlb_l2,page_walker_loads.dtlb_l3,page_walker_loads.dtlb_memory \
	  -e page_walker_loads.itlb_l1,page_walker_loads.itlb_l2,page_walker_loads.itlb_l3 \
	  -e l1d.replacement \
	  -e mem_load_uops_retired.l3_hit,mem_load_uops_l3_hit_retired.xsnp_hit,mem_load_uops_l3_hit_retired.xsnp_hitm,mem_load_uops_retired.l3_miss \
	  -e LLC-misses \
	  -e page-faults,minor-faults,major-faults \
	  -e l2_rqsts.all_pf,l2_rqsts.l2_pf_hit,l2_rqsts.l2_pf_miss \
	  --repeat 3 \
	  --output Statistics/test_perf_ubench_${1}_${2}.txt \
	  ./a.out ${1} ${2}
	  
		##-e offcore_response.all_pf_data_rd.any_response,offcore_response.all_pf_code_rd.any_response \
	  #-e offcore_response.pf_l2_data_rd.any_response,offcore_response.pf_l3_data_rd.any_response \
	  #-e L1-dcache-prefetches,L2-prefetches,LLC-prefetches \
		  
		  #./a.out ${1} ${2}

#   l2_rqsts.all_pf ==> [Requests from L2 hardware prefetchers]
#   l2_rqsts.l2_pf_hit ==> [L2 prefetch requests that hit L2 cache]
#   l2_rqsts.l2_pf_miss ==> [L2 prefetch requests that miss L2 cache]
#   offcore_response.all_pf_data_rd.any_response ==> [Counts all prefetch data reads that have any response type]
#   offcore_response.all_pf_code_rd.any_response ==> [Counts all prefetch code reads that have any response type]
#   offcore_response.pf_l2_data_rd.any_response  ==> [Counts all prefetch (that bring data to L2) data reads that have any response type]
#   offcore_response.pf_l3_data_rd.any_response  ==> [Counts all prefetch (that bring data to LLC only) data reads that have any response type]

########################################################################################################################################
######################################### Some Metrics #################################################################################
########################################################################################################################################

# (%) Cycles spent in page walks (data) = (DTLB_LOAD_MISSES.WALK DURATION + DTLB_STORE_MISSES.WALK DURATION) / CPU_CLK_UNHALTED.THREAD_P

# Page walks per 1000 instr. (data) = (DTLB_LOAD_MISSES.WALK_COMPLETED + DTLB_STORE_MISSES.WALK_COMPLETED) / (INST_RETIRED.ANY_P / 1000)

# Average cycles per page walk (data) = (DTLB_LOAD_MISSES.WALK_DURATION + DTLB_STORE_MISSES.WALK_DURATION) / (DTLB_LOAD_MISSES.WALK_COMPLETED + DTLB_STORE_MISSES.WALK_COMPLETED)

# (%) Cycles spent in page walks (instructions) = ITLB_MISSES.WALK_DURATION / CPU_CLK_UNHALTED.THREAD P

# Page walks per 1000 instr. (instructions) = ITLB_MISSES.WALK_COMPLETED * 1000 / INST_RETIRED.ANY_P

# Average cycles per page walk (instructions) = ITLB_MISSES.WALK_DURATION / ITLB_MISSES.WALK_COMPLETED

# L1 misses = L1D.REPLACEMENT

# L2 misses = MEM_LOAD_UOPS_RETIRED.LLC_HIT + MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_HIT + MEM_LOAD_UOPS_LLC_HIT_RETIRED.XSNP_HITM + MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS
 
# LLC misses = MEM_LOAD_UOPS_MISC_RETIRED.LLC_MISS
