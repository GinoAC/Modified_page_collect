import subprocess
import os

def check_running(benchmark):
	running = int(subprocess.check_output("ps -al | grep " + benchmark + " | wc -l",\
    stderr = subprocess.STDOUT, shell = True))
	
	#print(running)
	assert(running < 2)
	if running:
		return True
	else:
		return False

def get_pid(benchmark):
	pid = str(subprocess.check_output("ps -alh | grep " + benchmark,\
    stderr = subprocess.STDOUT, shell = True)).split()[2]
	return pid

EXE_PATH = "/media/ginochacon/gino/Benchmarks/gapbs/"
OUTPUT_PATH = "/media/ginochacon/gino/physical_machine_measurements/GAPS_results/"

GRAPHS_PATH = "/media/ginochacon/gino/Benchmarks/gapbs/benchmark/graphs/"

workloads = ["twitter", "web", "road", "kron", "urand"]
benchmark = {"bc" : "-i 4 -n 16 -f ", 
						"bfs" : "-n 64 -f ", 
						"cc" : "-n 16 -f ",
						"tc" : "-n 3 -f ",
						"sssp" : "-n 64 -d", 
						"pr" : "-i 1000 -t 1e-4 -f "} 

workloads_ext = {"bc" : ".sg", 
								"bfs" : ".sg", 
								"cc" : ".sg",
								"tc" : "U.sg",
								"sssp" : ".wsg",
								"pr" : ".sg"} 

sssp_delta = 	{"twitter" : "2 -f ", 
						 	"web" : "2 -f ", 
							"road" : "50000 -f ", 
							"kron" : "2 -f ", 
							"urand" : "2 -f "}

#launch each workload and measure with page-collect
for bm in benchmark.keys():
	for wl in workloads:
	
		#launch workloads
		if bm == "sssp":
			os.system(EXE_PATH + bm + " " + benchmark[bm] + " " + sssp_delta[wl] + " " + GRAPHS_PATH + wl + workloads_ext[bm] + " > " + OUTPUT_PATH + bm + "_" + wl + ".txt &")
			#print("." + EXE_PATH + bm + " " + benchmark[bm] + " " + sssp_delta[wl] + " " + wl + workloads_ext[bm] + " > " + OUTPUT_PATH + bm + "_" + wl + ".txt &")
		else:	
			os.system(EXE_PATH + bm + " " + benchmark[bm] + " " + GRAPHS_PATH + wl + workloads_ext[bm] + " > " + OUTPUT_PATH + bm + "_" + wl + ".txt &")
			print("." + EXE_PATH + bm + " " + benchmark[bm] + " " + wl + workloads_ext[bm] + " > " + OUTPUT_PATH + bm + "_" + wl + ".txt &")

		pid = get_pid(bm)
		#launch page collect	
		os.system("bash page-collect/collect_stats.sh " + pid + " GAPSB " + bm + " " + wl)
		print("bash page-collect/collect_stats.sh "+ pid + " GAPSB " + bm + " " + wl)
		running = check_running(bm)
		while running:
			running = check_running(bm)
		#os.system("./" + EXE_PATH + bm + " " + benchmark[bm] + " " + wl + workloads_ext[bm])

#sudo ./page-collect -p ${1} -o ${OUT_DIR}/pagecollect_ubench_${2}_${3}_${4}.txt # make sure that the stats are appended in the output file


#$(OUTPUT_DIR)/bfs-%.out : $(GRAPH_DIR)/%.sg bfs
#	./bfs -f $< -n64 > $@
#
#SSSP_ARGS = -n64
#$(OUTPUT_DIR)/sssp-twitter.out: $(GRAPH_DIR)/twitter.wsg sssp
#	./sssp -f $< $(SSSP_ARGS) -d2 > $@
#
#$(OUTPUT_DIR)/sssp-web.out: $(GRAPH_DIR)/web.wsg sssp
#	./sssp -f $< $(SSSP_ARGS) -d2 > $@
#
#$(OUTPUT_DIR)/sssp-road.out: $(GRAPH_DIR)/road.wsg sssp
#	./sssp -f $< $(SSSP_ARGS) -d50000 > $@
#
#$(OUTPUT_DIR)/sssp-kron.out: $(GRAPH_DIR)/kron.wsg sssp
#	./sssp -f $< $(SSSP_ARGS) -d2 > $@
#
#$(OUTPUT_DIR)/sssp-urand.out: $(GRAPH_DIR)/urand.wsg sssp
#	./sssp -f $< $(SSSP_ARGS) -d2 > $@
#
#$(OUTPUT_DIR)/pr-%.out: $(GRAPH_DIR)/%.sg pr
#	./pr -f $< -i1000 -t1e-4 -n16 > $@
#
#$(OUTPUT_DIR)/cc-%.out: $(GRAPH_DIR)/%.sg cc
#	./cc -f $< -n16 > $@
#
#$(OUTPUT_DIR)/bc-%.out: $(GRAPH_DIR)/%.sg bc
#	./bc -f $< -i4 -n16 > $@
#
#$(OUTPUT_DIR)/tc-%.out: $(GRAPH_DIR)/%U.sg tc
#	./tc -f $< -n3 > $@


