from typing import List

text_input = None

global_flags = {
    "files_loaded":{
        "bool":False,
        "error":"<b>The files must be loaded</b> before the aperture can be generated.<br><br>",
        "needing":[]
    },
    "circular_center":{
        "bool":False,
        "error":"<b>The circular centre must be calculated</b> before this step can be taken.",
        "needing":["files_loaded"]
    },
    "aperture":{
        "bool":False,
        "error":"<b>The circular centre must be calculated</b> before this step can be taken.",
        "needing":["files_loaded", "circular_center"]
    },   
}

def setup(self, widget):
    global text_input
    text_input = widget

def add_flag(flag:str):
    if not isinstance(flag, str):
        raise TypeError
    val = global_flags.get(flag, None)
    if val is None:
        raise KeyError
    else:
        global_flags[flag]["bool"] = not val["bool"]

def log(self, in_str:str, flag: str = None):
    if text_input:
        if not isinstance(in_str,str):
            raise TypeError
        if dict_bool:
            add_flag(flag)
        text_input.insertPlainText(in_str)
    else:
        raise RuntimeError("Text Input is not Defined")

def check_if_all_needed(current_flag: str, recursion:bool = False, display=True) -> bool:
    if not isinstance(current_flag, str):
        raise TypeError
    flag = global_flags.get(current_flag, None)
    if flag is None:
        raise KeyError
    if isinstance(flag, dict): #Should always be true
        if flag.get("bool", False):
            need = [(current_flag,True)]
            for el in flag.get("needing", []):
                need.append((el,check_if_all_needed(el, recursion=True)))
            if all([el[1] for el in need]):
                return True
        else:
            need = [(current_flag, False)]
        if not recursion:
            err = [global_flags.get(el[0]).get("error") for el in need]
            if display:
                err = "".join(err)
                QtWidgets.QMessageBox.warning(ApplicationWindow, "Warning",err)
            else:
                err = "\n".join(err)
                print(err)
        return False
    else:
        raise RuntimeError("An unknow error has happened. Did you modified the structure of globals_flags")
    

def clear(self):
    if text_input:
        text_input.setPlainText("")
        for key in global_flags.keys():
            global_flags[key]["bool"] = False
    else:
        raise RuntimeError("Text Input is not Defined")
