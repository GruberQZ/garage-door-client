import subprocess

args = ['ls']

output, errors = subprocess.Popen(args, stdout = subprocess.PIPE).communicate()

print(repr(output))