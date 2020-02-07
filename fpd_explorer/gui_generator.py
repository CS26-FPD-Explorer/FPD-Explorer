import inspect
from inspect import signature
from PySide2 import QtWidgets
from PySide2.QtWidgets import (QLineEdit, QPushButton, QFormLayout, QSpinBox, QCheckBox)


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
        result = {}
        """
        result is a dict with the variable name as key and a list composed of type, default value, description

        """
        param = doc.split('Parameters')[1].replace(',', '').replace(
            '-', '').split("Return")[0].split("Attributes")[0].split('\n')
        current_name = ""
        global_space = -1
        for idx, el in enumerate(param):
            if not el.isspace() and el:
                nb_space = len(el) - len(el.lstrip())
                if global_space == -1 and el.find(':') != -1:
                    global_space = nb_space
                if nb_space == global_space:
                    current_name, type = el.replace(' ', '').split(':')
                    default = sig.parameters[current_name]
                    if default is not None:
                        default = default.default
                        if default is inspect.Parameter.empty:
                            default = None
                    result[current_name] = [type, default]
                else:
                    result[current_name].append(param[idx].strip())
                    if len(result[current_name]) > 2:
                        result[current_name][2] = " ".join(result[current_name][2:])
                        del result[current_name][3:]
        return result

    def setup_ui(self):
        self.result = {}
        """
        self.widgets is a dictionary with the type as key and a list of widgets as val

        the list of widgets is compossed of a list compossed of key, widget, None value possible
        {
            type:[
                [key, widget, bool],
            ]
        }
        """
        self.widgets = {}
        for el in ["str", "int", "bool"]:
            self.widgets[el] = []
        for key, val in self.param.items():
            widget = None
            param_type = None
            if "array" in val[0]:
                # skip input that could be an array because its too hard to find a way to handle them
                print("skipping : ", val[0])
                continue
            elif "str" in val[0]:
                text = val[1] if val[1] is not None else key
                widget = QLineEdit(text)
                param_type = "str"
            elif "int" in val[0] or "scalar" in val[0]:
                default_val = val[1] if val[1] is not None else 0
                widget = QSpinBox()
                widget.setValue(default_val)
                param_type = "int"
            elif "bool" in val[0]:
                default_val = val[1] if val[1] is not None else False
                widget = QCheckBox()
                widget.setEnabled(default_val)
                param_type = "bool"
            else:
                print("TODO : Implement : ", val[0])
                continue
            none_possible = False
            if "None" in val[0]:
                none_possible = True
            widget.setToolTip(val[2])
            self.widgets[param_type].append([key, widget, none_possible])

        self.button = QPushButton("Save")
        # Create layout and add widgets
        layout = QFormLayout()
        for widgets in self.widgets.values():
            for key, widget, none_possible in widgets:
                layout.addRow(key.replace("_", " ").capitalize(), widget)

        layout.addRow(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.save)

    def save(self):
        for key, val in self.widgets.items():
            self.result[key] = val.text()
        print(self.result)
