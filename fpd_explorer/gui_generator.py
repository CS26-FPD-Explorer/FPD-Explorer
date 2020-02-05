import inspect
from inspect import signature
from PySide2 import QtWidgets
from PySide2.QtWidgets import (QLineEdit, QPushButton, QFormLayout, QSpinBox)
class UI_Generator(QtWidgets.QDialog):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    ApplicationWindow : QApplication
        The parent in which the tab should be rendered
    mainwindow : QMainWindow 
        The main window in which the dock widget should get created
    fnct : function
        The function object for which we want to create the input box

    """

    def __init__(self, application_window, main_window, fnct):
        super(UI_Generator, self).__init__()
        self.application_window = application_window
        self.main_window = main_window
        self.param = self.get_param_docstring(fnct)
        self.setup_ui()

    def get_param_docstring(self, fnct):
        sig = signature(fnct)
        doc = fnct.__doc__
        result = []
        tmp = []
        param = doc.split('Parameters')[1].replace(',','').replace('-','').split("Return")[0].split('\n')
        counter = 0
        for idx, el in enumerate(param):
            if not el.isspace() and el:
                if el.find(':') != -1:
                    if tmp != []:
                        result.append(tmp)
                        tmp = []
                    counter = 0
                    name, type = el.replace(' ', '').split(':')
                    default = sig.parameters[name]
                    if default is not None:
                        default = default.default
                        if default is inspect.Parameter.empty:
                            default = None
                    tmp.extend([name, type, default])
                if counter > 0:
                    tmp.append(param[idx].strip())
                    if len(tmp) > 3 :
                        tmp[3] = " ".join(tmp[3:])
                        del tmp[4:]
                counter += 1
        result.append(tmp)
        return result

    def setup_ui(self):
        self.result = {}
        self.widgets = {}
        for el in self.param:
            if "str" in el[1]:
                text = el[2] if el[2] is not None else el[0]
                self.widgets[el[0]] = QLineEdit(text)
            elif "int" in el[1]:
                val = el[2] if el[2] is not None else 0
                self.widgets[el[0]] = QSpinBox()
                self.widgets[el[0]].setValue(val)
            else:
                print("TODO : Implement : ", el[1])

            
        self.button = QPushButton("Save")
        # Create layout and add widgets
        layout = QFormLayout()
        for key, val in self.widgets.items():
            layout.addRow(key, val)

        layout.addRow(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.save)

    def save(self):
        for key, val in self.widgets.items():
            self.result[key] = val.text()
        print(self.result)

