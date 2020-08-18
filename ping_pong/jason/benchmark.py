
import subprocess
import psutil
import time

import glob, os, shutil

import re

JASON_PATH = None
for path in ["/home/mostafa/jason-latest/jason/build/scripts", "/Users/giovanni/opt/jason/scripts"]:
	if os.path.isdir(path):
		JASON_PATH = path

if JASON_PATH is None:
	raise RuntimeError("Not valid jason path")

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

def generate_meta(nbmatches, nbballs, delay, clean=True):

	print("generating test: Matches: %s, Balls: %s, Delay: %s" % (nbmatches, nbballs, delay))

	path = "M%s_B%s_D%s" % (nbmatches, nbballs, delay)

	if clean:
		remove_dir(path)

	make_dir(path)

	shutil.copyfile("./logging.properties", path+"/logging.properties")
	shutil.copytree("./actions", path+"/actions")

	asl_files = glob.glob("*.asl.meta")
	mas2j_files = glob.glob("*.mas2j.meta")

	for file in asl_files + mas2j_files:
		fin = open(file, "rt")
		fout = open(path + "/" + file.replace(".meta", ""), "wt")
		for line in fin:
			fout.write(line
					   .replace('__NBMATCHES__', str(nbmatches))
					   .replace('__NBBALLS__', str(nbballs))
					   .replace('__DELAY__', str(delay)))
		fin.close()
		fout.close()


def run_test(path, filename):

	print("run test: %s" % (path + "/" + filename))

	if not filename.endswith(".mas2j"):
		raise RuntimeError("wrong filename: %s" % filename)

	cpu_data = None

	start = time.time()
	psutil.cpu_percent(interval=0, percpu=True)
	command = [JASON_PATH+"/jason", path+"/"+filename]

	print("command: %s" % (" ".join(command)))

	try:
		output = subprocess.run(command, capture_output=True, timeout=60)
		cpu_data = psutil.cpu_percent(interval=0, percpu=True)
		print("CPU data: " + str(cpu_data))
		end = time.time()
		total_time = str(round((end - start) * 1000))
	except subprocess.TimeoutExpired:
		total_time = "TIMEOUT"
		internal_time = "TIMEOUT"

	print("total time elapsed (ms): " + total_time)

	if total_time != "TIMEOUT":
		start_pattern = re.compile("start at: (\d+)")
		end_pattern = re.compile("done at: (\d+)")

		string_output = str(output.stdout.decode('UTF-8'))
		print(output)

		start_found = False
		end_found = False

		for line in string_output.splitlines():
			if start_found is False:
				start_match = re.search(start_pattern, line)
				if start_match is not None:
					start_value = int(start_match.group(1))
					start_found = True
			else:
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

def main(BASE, MAXMATCHESLOG, MAXBALLSLOG, MAXDELAYLOG, REPETITIONS):
	evaluation_file = open(
		"../benchmark-jason-%d-%d-%d.csv" % (BASE ** MAXMATCHESLOG, BASE ** MAXBALLSLOG, MAXDELAYLOG), "w")
	evaluation_file.write("nbmatches;nbballs;delay;cpudata;total_time;internal_time\n")

	for i in range(1, MAXMATCHESLOG + 1, 1):  # iterating over numbers of agents
		nbmatches = BASE ** i
		for j in range(1, MAXBALLSLOG + 1, 1):  # iterating over numbers of tokens
			nbballs = BASE ** j
			for z in range(1, MAXDELAYLOG + 1, 1):  # iterating over numbers of tokens
				delay = BASE ** z
				for w in range(REPETITIONS):  # 10 executions to compute average and std_deviation
					generate_meta(nbmatches, nbballs, delay)
					cpudata, total_time, internal_time = run_test(
						"M%s_B%s_D%s" % (str(nbmatches), str(nbballs), str(delay)), "pingpong.mas2j")
					evaluation_file.write(
						str(nbmatches) + ";" + str(nbballs) + ";" + str(delay) + ";" + str(cpudata) + ";" + str(
							total_time) + ";" + str(internal_time) + "\n")

	evaluation_file.close()


if __name__ == "__main__":
	import sys

	if len(sys.argv) == 1:
		print("Usage: single [NBMATCHES] [NBBALLS] [DELAY]")
		print("Usage for iteration: [BASE] [MAXMATCHESLOG] [MAXBALLSLOG] [MAXDELAYLOG] [REPETITIONS]")

	elif sys.argv[1] == "single":
		if len(sys.argv) != 5:
			print("Usage: single [NBMATCHES] [NBBALLS] [DELAY]")
		else:
			nbmatches = int(sys.argv[2])
			nbballs = int(sys.argv[3])
			delay = int(sys.argv[4])
			generate_meta(nbmatches, nbballs, delay)
			cpudata, total_time, internal_time = run_test("M%s_B%s_D%s" % (str(nbmatches), str(nbballs), str(delay)),
														  "pingpong.mas2j")
			print("CPU data: %s" % str(cpudata))
			print("Total time: %s" % str(total_time))
			print("Internal time: %s" % str(internal_time))
	else:
		if len(sys.argv) != 6:
			print("Usage for iteration: [BASE] [MAXMATCHESLOG] [MAXBALLSLOG] [MAXDELAYLOG] [REPETITIONS]")
		else:
			main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
