# Dirty file to automatically compile all .ui files

# Standard Library
import os
import subprocess
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk("./fpd_explorer/res/"):
    f.extend([os.path.join(*dirpath.split("/"), s) for s in filenames])
tmp = [el for el in f if el[-3:] == ".ui"]
print(f"Found {len(tmp)} files: Compiling.....")
for el in f:
    file_path, ext = os.path.splitext(el)
    file = os.path.split(file_path)
    new_file = os.path.join(*file[:-1], "ui_" + file[-1] + ".py")
    if ext == ".ui":
        print(f"Compiling {el} to {new_file} ... ")
        subprocess.run("pyside2-uic -o " + new_file + " " + el, shell=True, check=True)
