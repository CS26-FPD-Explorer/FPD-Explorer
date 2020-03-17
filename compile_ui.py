# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.

# Standard Library
import os
import subprocess
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk("./fpd_explorer/frontend/res/"):
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
