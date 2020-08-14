
import subprocess
import psutil
import time

import glob, os, shutil

import re

ASTRAJAR_PATH = "/Users/giovanni/dev/benchmark/token_ring/source_files/astra/exec"
# ASTRAJAR_PATH = "/home/mostafa/benchmark/token_ring/source_files/astra/exec"

def run_test(nbagents, nbtokens, nbconsumptions):

	print("starting test: Workers: %s, Tokens: %s, Consumptions: %s" % (nbagents, nbtokens, nbconsumptions))

	start = time.time()
	psutil.cpu_percent(interval=0, percpu=True)
	command = ["java", "-jar", ASTRAJAR_PATH+"/ASTRA_tokens.jar", str(nbtokens), str(nbagents)]
	output = subprocess.run(command, capture_output=True)
	cpu_data = psutil.cpu_percent(interval=0, percpu=True)
	print("CPU data: " + str(cpu_data))
	end = time.time()
	total_time = str((end - start) * 1000)
	print("total time elapsed (ms): " + total_time)

	start_pattern = re.compile("time:(\d+)")
	end_pattern = re.compile("time:(\d+)")

	string_output = str(output.stdout.decode('UTF-8'))

	print(output)

	start_found = False
	end_found = False

	for line in string_output.splitlines():
		if start_found and end_found:
			break
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

evaluation_file = open("benchmark.csv", "w")
evaluation_file.write("nbagents;nbtokens;nbconsumptions;cpudata;total_time;internal_time\n")

for i in range(1, 3, 1): # iterating over numbers of agents
	nbagents = 10**i
	for j in range(0, 3, 1): # iterating over numbers of tokens
		nbtokens = 10 ** j
		for z in range(0, 3, 1): # iterating over numbers of consumptions
			nbconsumptions = 10 ** z

			for w in range (2): # 10 executions to compute average and std_deviation
				cpudata, total_time, internal_time = run_test(nbagents, nbtokens, nbconsumptions)
				evaluation_file.write(str(nbagents) + ";" + str(nbtokens) + ";" + str(nbconsumptions) + ";" + str(cpudata) + ";" + str(total_time) + ";" + str(internal_time) + "\n")

evaluation_file.close()