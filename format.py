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
