import inspect
from inspect import signature
from PySide2 import QtWidgets
from PySide2.QtWidgets import QLineEdit, QPushButton, QFormLayout, QSpinBox, QCheckBox, QDialogButtonBox, QGridLayout
from PySide2.QtCore import Qt


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

    def __init__(self, application_window, main_window, fnct, items_per_column=10):
        super(UI_Generator, self).__init__()
        self.application_window = application_window
        self.main_window = main_window
        self.param = self.get_param(fnct)
        self.items_per_column = items_per_column
        self.setup_ui()

    def get_param(self, fnct):
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
            ],
        }
        """
        self.widgets = {}
        self.default = {}
        for el in ["str", "int", "bool"]:
            self.widgets[el] = []
        for key, val in self.param.items():
            widget = None
            param_type = None
            if "array" in val[0] or "length" in val[0]:
                # skip input that could be an array because its too hard to find a way to handle them
                print("skipping : ", val[0])
                continue
            elif "str" in val[0]:
                default_val = val[1] if val[1] is not None else key
                widget = QLineEdit()
                widget.setPlaceholderText(self.set_default(widget, default_val))
                param_type = "str"
            elif "int" in val[0] or "scalar" in val[0]:
                default_val = val[1] if val[1] is not None else 0
                widget = QSpinBox()
                widget.setValue(self.set_default(widget, default_val))
                widget.setMinimum(-1000)
                widget.setMaximum(1000)
                param_type = "int"
            elif "bool" in val[0]:
                default_val = val[1] if val[1] is not None else False
                widget = QCheckBox()
                widget.setChecked(self.set_default(widget, default_val))
                param_type = "bool"
            else:
                print("TODO : Implement : ", val[0])
                continue
            none_possible = False
            if "None" in val[0]:
                none_possible = True
            widget.setToolTip(val[2])
            self.widgets[param_type].append([key, widget, none_possible])
        self.format_layout()

    def save(self):
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    self.result[key] = widget.isChecked()
                elif param_type == "int":
                    tmp = widget.value()
                    if none_possible and tmp == 0:
                        tmp = None
                    self.result[key] = tmp
                else:
                    self.result[key] = widget.text()
        print(self.result)
        self.accept()

    def set_default(self, widget, default_val):
        self.default[widget] = default_val
        return default_val

    def restore_default(self):
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    widget.setChecked(self.default[widget])
                elif param_type == "int":
                    widget.setValue(self.default[widget])
                else:
                    widget.clear()
                    widget.setPlaceholderText(self.default[widget])

    def format_layout(self):
        # Create layout and add widgets
        all_widget = []
        for widgets in self.widgets.values():
            for key, widget, none_possible in widgets:
                widget.setFixedHeight(30)
                all_widget.append((key.replace("_", " ").capitalize(), widget))
                #self.layout.addRow(key.replace("_", " ").capitalize(), widget)

        self.layout = QGridLayout()

        self.create_colums(all_widget, self.layout)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save
                                        | QDialogButtonBox.Cancel
                                        | QDialogButtonBox.RestoreDefaults)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_default)
        
        self.layout.addWidget(self.buttonBox, 1, 0, 1,3, Qt.AlignRight)
        self.setLayout(self.layout)
        self.setFixedSize(self.width(), self.minimumHeight())

    def create_colums(self, widget_list, vert_layout, n=0):
        tmp = QtWidgets.QWidget()
        layout = QFormLayout()
        for name, widget in widget_list[0+self.items_per_column*n:self.items_per_column+self.items_per_column*n]:
            layout.addRow(name, widget)
        tmp.setLayout(layout)
        vert_layout.addWidget(tmp, 0, n)
        if self.items_per_column*n > len(widget_list):
            return
        self.create_colums(widget_list, vert_layout, n=n+1)
