from concurrent.futures import thread
import subprocess
import multiprocessing, signal
import time



def run(config:str):
    filename = "heistbot4.py"
    while True:
        p = subprocess.Popen(f"python {filename} {config}", shell=True)
        p.wait()
        
        if p!=0:
            continue
        
if __name__ == "__main__":
    multi = []
    configs = ['bot1', 'bot2', 'bot3']
    try:
        for config in configs:
            one_process = multiprocessing.Process(target=run, args=(config,))
            multi.append(one_process)
            one_process.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for p in multi:
            p.terminate()
            p.exitcode == -signal.SIGTERM