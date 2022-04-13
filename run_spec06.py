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

EXE_PATH = "/media/ginochacon/gino/Benchmarks/spec_test/benchspec/CPU2006/"
OUTPUT_PATH = "/media/ginochacon/gino/physical_machine_measurements/SPEC06_results/"

bm_names = ["perlbench", "gcc", "bwaves", "gamess", "mcf", "milc", "zeusmp", 
						"gromacs", "cactusADM", "leslie3d", "namd", "gobmk", "soplex", 
						"povray", "calculix", "hmmer", "sjeng",
						"libquantum", "h264ref", "tonto", "lbm", "omnetpp", "astar", 
						"wrf", "sphinx3", "xalancbmk", "specrand_i", "specrand_f"]
#"bzip2","GemsFDTD" 

run_subdir = "/run/run_base_ref_amd64-m64-gcc43-nn.0000/"
exe_subname = "_base.amd64-m64-gcc43-nn"

run_dir_num = {	"perlbench" : "400.", "bzip2" : "401.", "gcc" : "403.",\
								"bwaves" : "410.", "gamess" : "416.", "mcf" : "429.",\
								"milc" : "433.", "zeusmp" : "434.", "gromacs" : "435.",\
								"cactusADM" : "436.", "leslie3d" : "437.", "namd" : "444.",\
								"gobmk" : "445.", "soplex" : "450.", "povray" : "453.",\
								"calculix" : "454.", "hmmer" : "456.", "sjeng" : "458.",\
								"GemsFDTD" : "459.", "libquantum" : "462.", "h264ref" : "464.",\
								"tonto" : "465.", "lbm" : "470.", "omnetpp" : "471.", "astar" : "473.",\
								"wrf" : "481.", "sphinx3" : "482.", "xalancbmk" : "483.",\
								"specrand_i" : "998.", "specrand_f" : "999."}

input_vals = {	"perlbench" 	: "-I./lib checkspam.pl 2500 5 25 11 150 1 1 1 1", 
								"bzip2" 			: "input.source 280", 
								"gcc" 				: "166.i -o 166.s",
								"bwaves" 			: "", 
								"gamess" 			: "cytosine.2.config", 
								"mcf" 				: "inp.in",
								"milc" 				: "su3imp.in", 
								"zeusmp" 			: "", 
								"gromacs" 		: "-silent -deffnm gromacs -nice 0",\
								"cactusADM" 	: "benchADM.par", 
								"leslie3d" 		: "", 
								"namd" 				: "--input namd.input --output namd.out --iterations 38",\
								"gobmk" 			: "--quiet --mode gtp", 
								"soplex" 			: "-m45000 pds-50.mps", 
								"povray" 			: "SPEC-benchmark-ref.ini",\
								"calculix" 		: "-i hyperviscoplastic", 
								"hmmer" 			: "nph3.hmm swiss41", 
								"sjeng" 			: "ref.txt",\
								"GemsFDTD" 		: "",
								"libquantum" 	: "1397 7", 
								"h264ref" 		: "-d foreman_ref_encoder_baseline.cfg",\
								"tonto" 			: "", 
								"lbm" 				: "300 reference.dat 0 0 100_100_130_ldc.of", 
								"omnetpp" 		: "omnetpp.ini", 
								"astar" 			: "rivers.cfg",\
								"wrf" 				: "", 
								"sphinx3" 		: "ctlfile . args.an4", 
								"xalancbmk" 	: "-v t5.xml xalanc.xsl",\
								"specrand_i" 	: "1255432124 234923", 
								"specrand_f" 	: "1255432124 234923"} 
#launch form:
#"EXE_PATH + run_dir_num[bench] + bench + run_subdir + bench + exe_subname " + input_vals[bench]

cwd = os.getcwd()

#launch each workload and measure with page-collect
for bm in sorted(bm_names):
	exe_dir = EXE_PATH + run_dir_num[bm] + bm + run_subdir

	print("Moving to dir: " + exe_dir)
	os.chdir(exe_dir)

	#launch job from SPEC working dir
	os.system(exe_dir + bm + exe_subname + " " + input_vals[bm] + " > " + OUTPUT_PATH + bm + ".txt &")

	#move back to measurements directory
	os.chdir(cwd)

	pid = get_pid(bm)
	#launch page collect	
	os.system("bash page-collect/collect_stats.sh " + pid + " SPEC06 " + bm + " " + " ")
	print("bash page-collect/collect_stats.sh "+ pid + " SPEC06 " + bm + " " + " ")
	running = check_running(bm)
	while running:
		running = check_running(bm)
	#exit()
