
import subprocess
import psutil
import time

import glob, os

JASON_PATH = "/Users/giovanni/opt/jason/scripts"

def make_dir(path):
	if not os.path.isdir(path):
		try:
			os.mkdir(path)
		except OSError:
			raise RuntimeError("Creation of the directory %s failed" % path)

def generate_meta(nbagents, nbtokens):
	os.chdir("./")
	output_path = "W%s_T%s" % (nbagents, nbtokens)

	make_dir(output_path)

	asl_files = glob.glob("*.asl.meta")
	mas2j_files = glob.glob("*.mas2j.meta")

	for file in asl_files + mas2j_files:
		fin = open(file, "rt")
		fout = open(output_path + "/" + file.replace(".meta", ""), "wt")
		for line in fin:
			fout.write(line.replace('__NBAGENTS__', str(nbagents)).replace('__NBTOKENS__', str(nbtokens)))
		fin.close()
		fout.close()


def run_test(filename):
	if not filename.endswith(".mas2j"):
		print("Wrong filename: %s" % filename)
	else: 
		start = time.time_ns()
		psutil.cpu_percent(interval=0, percpu=True)
		subprocess.run([JASON_PATH+"/jason", filename])
		print(psutil.cpu_percent(interval=0, percpu=True))
		end = time.time_ns()
		print ((end - start) / (10 ** 9 ))


nbagents = 2
nbtokens = 250
generate_meta(nbagents, nbtokens)
run_test("W%s_T%s/threadring_with_distributor.mas2j" % (str(nbagents), str(nbtokens)))