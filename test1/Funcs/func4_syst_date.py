import subprocess
import io


sp = subprocess.Popen(['DATE'], stdout = subprocess.PIPE, shell=True)

print(sp)

out = io.TextIOWrapper(sp.stdout, encoding='cp866')

s = ' '

while s:
    s = out.readline()
    print(s)

