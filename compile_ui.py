# Dirty file to automatically compile all .ui files

from os import walk
import os
f = []
for (dirpath, dirnames, filenames) in walk("./"):
    f.extend(filenames)
    break
for el in f:
    splitted = el.split(".")
    if splitted[1] == "ui":
        os.system("pyside2-uic " + el + " > ui_" + splitted[0] + ".py")
