# Standard Library
import os
import subprocess
from os import walk

f = []
exclude = ["res", "custom_fpd_lib", "tests"]
for (dirpath, dirnames, filenames) in walk("./", topdown=True):
    dirnames[:] = [d for d in dirnames if d not in exclude]
    f.extend([os.path.join(*dirpath.split("/"), s) for s in filenames])
tmp = [el for el in f if el[-3:] == ".py"]
print(f"Found {len(tmp)} files: Compiling.....")
for el in tmp:
    print(f"========== Formatting {el}")
    subprocess.run("autoflake --in-place --remove-all-unused-imports " + el, shell=True, check=True)
    subprocess.run("isort " + el, shell=True, check=True)
    subprocess.run("autopep8 --in-place --aggressive --aggressive " + el, shell=True, check=True)
