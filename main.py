import subprocess

filename = "heistbot4.py"
get_str = input("Enter the name of the file: ")
while True:
    print(f"python {filename} {get_str} ")
    p = subprocess.Popen(f"python {filename} {get_str}", shell=True).wait()
    
    if p!=0:
        continue    