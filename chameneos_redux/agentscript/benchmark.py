
import subprocess
import psutil
import time

import glob, os, shutil

import re

SCRIPTCC_PATH = None
for path in ["/home/mostafa/benchmark", "/Users/giovanni/dev/benchmark"]:
	if os.path.isdir(path):
		SCRIPTCC_PATH = path

if SCRIPTCC_PATH is None:
	raise RuntimeError("Not valid scriptcc path")

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

def generate_meta(nbagents, nbmeetings, clean=True):

	print("generating test: Chameneos: %s, Meetings: %s" % (nbagents, nbmeetings))

	path = "C%s_M%s" % (nbagents, nbmeetings)

	if clean:
		remove_dir(path)

	make_dir(path)

	ascript_files = glob.glob("*.ascript.meta")
	json_files = glob.glob("*.json.meta")

	for file in ascript_files + json_files:
		fin = open(file, "rt")
		fout = open(path + "/" + file.replace(".meta", ""), "wt")
		for line in fin:
			fout.write(line
					   .replace('__NBAGENTS__', str(nbagents))
					   .replace('__NBMEETINGS__', str(nbmeetings)))
		fin.close()
		fout.close()


def run_test(path, filename):

	print("run test: %s" % (path + "/" + filename))

	if not filename.endswith(".json"):
		raise RuntimeError("wrong filename: %s" % filename)

	cpu_data = None

	start = time.time()
	psutil.cpu_percent(interval=0, percpu=True)
	command = ["java", "-cp", SCRIPTCC_PATH+"/grounds-assembly-0.1.0-SNAPSHOT.jar:cham_data_test-1.0.jar", "scriptcc.Main", path+"/"+filename]

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
		start_pattern = re.compile("start at:")
		number_pattern = re.compile("(\d+)")
		end_pattern = re.compile("done at:")

		string_output = str(output.stdout.decode('UTF-8'))

		print(output)

		start_found = False
		end_found = False
		number = False
		for line in string_output.splitlines():
			if start_found and end_found:
				number_match = re.search(number_pattern, line)
				if number_match is not None:
					end_value = int(number_match.group(1))
					break
			if start_found is False:
				start_match = re.search(start_pattern, line)
				if start_match is not None:
					start_found = True
					number = True
			else:
				if number is True:
					number_match = re.search(number_pattern, line)
					if number_match is not None:
						start_value = int(number_match.group(1))
						number = False
				else:
					end_match = re.search(end_pattern, line)
					if end_match is not None:
						end_found = True
						number = True

		if start_found is False or end_found is False:
			raise RuntimeError("Unexpected result (no or partial time signatures).")

		internal_time = end_value - start_value
		print("internal time elapsed (ms): " + str((internal_time)))

	return (cpu_data, total_time, internal_time)

# ------------ main

def main(BASE, MAXAGENTSLOG, MAXMEETINGSLOG, REPETITIONS):

	evaluation_file = open("../benchmark-agentscript-%d-%d.csv" % (BASE**MAXAGENTSLOG, BASE**MAXMEETINGSLOG), "w")
	evaluation_file.write("nbagents;nbmeetings;cpudata;total_time;internal_time\n")

	for i in range(3, MAXAGENTSLOG + 1, 1): # iterating over numbers of agents
		nbagents = BASE**i
		for j in range(4, MAXMEETINGSLOG + 1, 1): # iterating over numbers of tokens
			nbmeetings = BASE**j
			for w in range(REPETITIONS): # 10 executions to compute average and std_deviation
				generate_meta(nbagents, nbmeetings)
				cpudata, total_time, internal_time = run_test("C%s_M%s" % (str(nbagents), str(nbmeetings)), "input.json")
				evaluation_file.write(str(nbagents) + ";" + str(nbmeetings) + ";" + str(cpudata) + ";" + str(total_time) + ";" + str(internal_time) + "\n")
	
	evaluation_file.close()


if __name__ == "__main__":
	import sys

	if len(sys.argv) == 1:
		print("Usage: single [NBAGENTS] [NBMEETINGS]")
		print("Usage for iteration: [BASE] [MAXAGENTSLOG] [MAXMEETINGSLOG] [REPETITIONS]")

	elif sys.argv[1] == "single":
		if len(sys.argv) != 4:
			print("Usage: single [NBAGENTS] [NBMEETINGS]")
		else:
			nbagents = int(sys.argv[2])
			nbmeetings = int(sys.argv[3])
			generate_meta(nbagents, nbmeetings)
			cpudata, total_time, internal_time = run_test("C%s_M%s" % (str(nbagents), str(nbmeetings)), "input.json")
			print("CPU data: %s" % str(cpudata))
			print("Total time: %s" % str(total_time))
			print("Internal time: %s" % str(internal_time))
	else:
		if len(sys.argv) != 5:
			print("Usage: [BASE] [MAXAGENTSLOG] [MAXMEETINGSLOG] [REPETITIONS]")
		else:
			main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
