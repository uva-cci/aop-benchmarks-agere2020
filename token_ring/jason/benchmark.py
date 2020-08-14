
import subprocess
import psutil
import time

import glob, os, shutil

import re

# JASON_PATH = "/Users/giovanni/opt/jason/scripts"
JASON_PATH = "/home/mostafa/jason/scripts"

def remove_dir(path):
	if os.path.isdir(path):
		try:
			shutil.rmtree(path)
		except OSError as e:
			raise RuntimeError("error in removing directory: %s -- %s" % (path, e.strerror))

def make_dir(path):
	if not os.path.isdir(path):
		try:
			os.mkdir(path)
		except OSError as e:
			raise RuntimeError("error in creating directory: %s -- %s" % (path, e.strerror))

def generate_meta(nbagents, nbtokens, nbhops, clean=True):

	print("generating test: Workers: %s, Tokens: %s, Consumptions: %s" % (nbagents, nbtokens, nbhops))

	path = "W%s_T%s_C%s" % (nbagents, nbtokens, nbhops)

	if clean:
		remove_dir(path)

	make_dir(path)

	shutil.copyfile("./logging.properties", path+"/logging.properties")

	asl_files = glob.glob("*.asl.meta")
	mas2j_files = glob.glob("*.mas2j.meta")

	for file in asl_files + mas2j_files:
		fin = open(file, "rt")
		fout = open(path + "/" + file.replace(".meta", ""), "wt")
		for line in fin:
			fout.write(line
					   .replace('__NBAGENTS__', str(nbagents))
					   .replace('__NBTOKENS__', str(nbtokens))
					   .replace('__NBCONSUMPTIONS__', str(nbhops)))
		fin.close()
		fout.close()


def run_test(path, filename):

	if not filename.endswith(".mas2j"):
		raise RuntimeError("wrong filename: %s" % filename)

	start = time.time()
	psutil.cpu_percent(interval=0, percpu=True)
	subprocess.run([JASON_PATH+"/jason", path+"/"+filename])
	cpu_data = psutil.cpu_percent(interval=0, percpu=True)
	print("CPU data: " + str(cpu_data))
	end = time.time()
	total_time = str((end - start) * 1000)
	print("total time elapsed (ms): " + total_time)

	start_pattern = re.compile("start\((\d+)\)\.")
	end_pattern = re.compile("end\((\d+)\)\.")

	start_found = False
	end_found = False
	for i, line in enumerate(open(path+"/distributor-FINALSNAPSHOT.asl")):
		if start_found and end_found:
			break
		start_match = re.search(start_pattern, line)
		if start_match is not None:
			start_value = int(start_match.group(1))
			start_found = True
		end_match = re.search(end_pattern, line)
		if end_match is not None:
			end_value = int(end_match.group(1))
			end_found = True

	if start_found is False or end_found is False:
		raise RuntimeError("Unexpected result (no or partial time signatures).")

	internal_time = end_value - start_value
	print("internal time elapsed (ms): " + str((internal_time)))

	return (cpu_data, total_time, internal_time)

# ------------ main

def main(BASE, MAXAGENTSLOG, MAXTOKENSLOG, MAXHOPSLOG, REPETITIONS):

	evaluation_file = open("benchmark-%d-%d-%d.csv" % (BASE**MAXAGENTSLOG, BASE**MAXAGENTSLOG, BASE**MAXHOPSLOG), "w")
	evaluation_file.write("nbagents;nbtokens;nbhops;cpudata;total_time;internal_time\n")

	for i in range(1, MAXAGENTSLOG, 1): # iterating over numbers of agents
		nbagents = BASE**i
		for j in range(1, MAXTOKENSLOG, 1): # iterating over numbers of tokens
			nbtokens = BASE**j
			for z in range(1, MAXHOPSLOG, 1): # iterating over numbers of consumptions
				nbhops = BASE**z

				for w in range(REPETITIONS): # 10 executions to compute average and std_deviation
					generate_meta(nbagents, nbtokens, nbhops)
					cpudata, total_time, internal_time = run_test("W%s_T%s_C%s" % (str(nbagents), str(nbtokens), str(nbhops)), "threadring_with_distributor.mas2j")
					evaluation_file.write(str(nbagents) + ";" + str(nbtokens) + ";" + str(nbhops) + ";" + str(cpudata) + ";" + str(total_time) + ";" + str(internal_time) + "\n")

	evaluation_file.close()


if __name__ == "__main__":
	import sys
	if len(sys.argv) != 6:
		print("Usage: [BASE] [MAXAGENTSLOG] [MAXTOKENSLOG] [MAXHOPSLOG] [REPETITIONS]")
	else:
		main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
