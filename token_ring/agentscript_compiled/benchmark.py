
import subprocess
import psutil
import time

import glob, os, shutil

import re

SCALAJAR_PATH = None
for path in ["/home/mostafa/benchmark/token_ring/agentscript_compiled/exec", "/Users/giovanni/dev/benchmark/token_ring/agentscript_compiled/exec"]:
	if os.path.isdir(path):
		SCALAJAR_PATH = path

if SCALAJAR_PATH is None:
	raise RuntimeError("Not valid scala jar path")

def run_test(nbagents, nbtokens, nbhops):

	print("starting test: Workers: %s, Tokens: %s, Hops: %s" % (nbagents, nbtokens, nbhops))

	cpu_data = None

	start = time.time()
	psutil.cpu_percent(interval=0, percpu=True)
	command = ["java", "-server", "-cp", SCALAJAR_PATH+"/grounds_benchmarks.jar", "benchmark.Token_ring", str(nbtokens), str(nbagents), str(nbhops)]

	try:
		output = subprocess.run(command, capture_output=True, timeout=120)
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
				end_value = int(number_match.group(1))
				break
			if start_found is False:
				start_match = re.search(start_pattern, line)
				if start_match is not None:
					start_found = True
					number = True
			else:
				if number:
					number_match = re.search(number_pattern, line)
					start_value = int(number_match.group(1))
					number = False
				else:
					end_match = re.search(end_pattern, line)
					if end_match is not None:
						end_found = True

		if start_found is False or end_found is False:
			raise RuntimeError("Unexpected result (no or partial time signatures).")

		internal_time = end_value - start_value
		print("internal time elapsed (ms): " + str((internal_time)))

	return (cpu_data, total_time, internal_time)

# ------------ main

def main(BASE, MAXAGENTSLOG, MAXTOKENSLOG, MAXHOPSLOG, REPETITIONS):

	evaluation_file = open("../benchmark-agentscript_compiled-%d-%d-%d.csv" % (BASE**MAXAGENTSLOG, BASE**MAXTOKENSLOG, BASE**MAXHOPSLOG), "w")
	evaluation_file.write("nbagents;nbtokens;nbhops;cpudata;total_time;internal_time\n")

	for i in range(1, MAXAGENTSLOG + 1, 1): # iterating over numbers of agents
		nbagents = BASE**i
		for j in range(1, MAXTOKENSLOG + 1, 1): # iterating over numbers of tokens
			nbtokens = BASE**j
			for z in range(1, MAXHOPSLOG + 1, 1): # iterating over numbers of consumptions
				nbhops = BASE**z

				for w in range(REPETITIONS): # 10 executions to compute average and std_deviation
					cpudata, total_time, internal_time = run_test(nbagents, nbtokens, nbhops)
					evaluation_file.write(str(nbagents) + ";" + str(nbtokens) + ";" + str(nbhops) + ";" + str(cpudata) + ";" + str(total_time) + ";" + str(internal_time) + "\n")

	evaluation_file.close()


if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		print("Usage: single [NBAGENTS] [NBTOKENS] [NBHOPS]")
		print("Usage for iteration: [BASE] [MAXAGENTSLOG] [MAXMEETINGSLOG] [REPETITIONS]")
	elif sys.argv[1] == "single":
		if len(sys.argv) != 5:
			print("Usage: single [NBAGENTS] [NBTOKENS] [NBHOPS]")
		else:
			nbagents = int(sys.argv[2])
			nbtokens = int(sys.argv[3])
			nbhops = int(sys.argv[4])
			cpudata, total_time, internal_time = run_test(nbagents, nbtokens, nbhops)
			print("CPU data: %s" % str(cpudata))
			print("Total time: %s" % str(total_time))
			print("Internal time: %s" % str(internal_time))
	else:
		if len(sys.argv) != 6:
			print("Usage: [BASE] [MAXAGENTSLOG] [MAXTOKENSLOG] [MAXHOPSLOG] [REPETITIONS]")
		else:
			main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
