
import subprocess
import psutil
import time

start = time.time_ns()
psutil.cpu_percent(interval=0, percpu=True)
subprocess.run(["/home/msotafa/IdeaProjects/jason/scripts/jason","/home/msotafa/IdeaProjects/jason/examples/ring/threadring.mas2j"])
print(psutil.cpu_percent(interval=0, percpu=True))
end = time.time_ns()
print ((end - start) / (10 ** 9 ))