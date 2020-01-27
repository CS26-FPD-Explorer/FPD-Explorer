from typing import List

text_input = None
def setup(self, widget):
    global text_input
    text_input = widget

def log(self, in_str:str):
    if text_input:
        if not isinstance(in_str,str):
            raise TypeError
        text_input.insertPlainText(in_str)
    else:
        raise RuntimeError("Text Input is not Defined")


def clear(self):
    if text_input:
        text_input.setPlainText("")
    else:
        raise RuntimeError("Text Input is not Defined")
