# Dirty file to automatically compile all .ui files

from os import walk
import subprocess

import os
f = []
for (dirpath, dirnames, filenames) in walk("./resources/"):
    f.extend([os.path.join(*dirpath.split("/"), s) for s in filenames])

print(f"Found {len(f)} files: Compiling.....")
for el in f:
    file_path, ext = os.path.splitext(el)
    file = os.path.split(file_path)[-1]
    if ext == ".ui":
        print(f"Compiling {el} to ui_{file}.py ... ")
        subprocess.run("pyside2-uic -o " + "ui_" + file + ".py " + el , capture_output=True, check=True)
