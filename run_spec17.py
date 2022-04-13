import subprocess
import os

def check_running(benchmark):
	running = int(subprocess.check_output("ps -alh | grep " + benchmark + " | grep -v \/bin | grep -v grep | wc -l",\
    stderr = subprocess.STDOUT, shell = True))
	
	print("running " + str(running))
	#assert(running < 2)
	if running:
		return True
	else:
		return False
bm_run_names = {"523.xalancbmk_r" : "cpuxalan_r_base"}

def get_pid(benchmark):
	#print("ps -alh | grep " + benchmark + " | grep -v \/bin")
	pres = int(subprocess.check_output("ps -alh | grep " + benchmark + " | grep -v \/bin | grep -v grep | wc -l",\
													 stderr = subprocess.STDOUT, shell = True))

	#os.system("ps -alh | grep " + benchmark + " | grep -v \/bin")
	#print(pres)
	if not pres:
		return 0
	else:
		pid = str(subprocess.check_output("ps -alh | grep " + benchmark + " | grep -v \/bin",\
			stderr = subprocess.STDOUT, shell = True)).split()[2]
	return pid

EXE_PATH = "/media/ginochacon/gino/Benchmarks/spec_17/"
OUTPUT_PATH = "/media/ginochacon/gino/physical_machine_measurements/SPEC17_results/"

CONFIG = "GAC_linux_x86.cfg"

bm_names = ["500.perlbench_r", "502.gcc_r", "503.bwaves_r", "505.mcf_r", "508.namd_r", "511.povray_r",
						"519.lbm_r", "520.omnetpp_r", "521.wrf_r", "525.x264_r", "526.blender_r", "527.cam4_r", "531.deepsjeng_r",
						"538.imagick_r", "541.leela_r", "544.nab_r", "548.exchange2_r", "549.fotonik3d_r", "554.roms_r", "557.xz_r", "600.perlbench_s",
						"602.gcc_s", "603.bwaves_s", "605.mcf_s", "619.lbm_s", "620.omnetpp_s", "621.wrf_s", "625.x264_s", "627.cam4_s", 
						"631.deepsjeng_s", "638.imagick_s", "641.leela_s", "644.nab_s", "648.exchange2_s",
						"649.fotonik3d_s", "654.roms_s", "657.xz_s"]

#"607.cactusBSSN_s", "507.cactusBSSN_r", "510.parest_r","523.xalancbmk_r",  "623.xalancbmk_s","628.pop2_s", 
#launch form:

cwd = os.getcwd()

cmd = "runcpu --config=GAC_linux_x86.cfg " 

#launch each workload and measure with page-collect
for bm in sorted(bm_names):
	print("Moving to dir: " + EXE_PATH)
	os.chdir(EXE_PATH)

	#launch job from SPEC working dir
	os.system(cmd + bm + " > " + OUTPUT_PATH + bm + ".txt &")

	#move back to measurements directory
	os.chdir(cwd)

	pid = get_pid(bm[4:-2])
	print("Waiting for " + bm + " to launch")
	while pid == 0:
		pid = get_pid(bm[4:-2])
	print(pid)
	#launch page collect	
	os.system("bash page-collect/collect_stats.sh " + pid + " SPEC17 " + bm + " " + " ")
	running = check_running(bm)
	while running:
		running = check_running(bm)
