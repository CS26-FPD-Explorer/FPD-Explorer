# Standard Library
import inspect
from inspect import signature
from collections import defaultdict

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QSpinBox,
    QCheckBox,
    QLineEdit,
    QFormLayout,
    QGridLayout,
    QVBoxLayout,
    QDoubleSpinBox,
    QDialogButtonBox
)


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

    def __init__(self, application_window, fnct, items_per_column=10, key_ignore=None, key_add=None):
        super(UI_Generator, self).__init__()
        self.application_window = application_window
        self.key_ignore = key_ignore
        self.key_add = key_add
        self.param = self._get_param(fnct)
        self.items_per_column = items_per_column
        self.default = {}
        self._setup_ui()
        self.setWindowFlags((self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint) & ~Qt.WindowContextHelpButtonHint)

    def _get_param(self, fnct):
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
        if self.key_ignore is not None:
            [result.pop(x, None) for x in self.key_ignore]
        if self.key_add is not None:
            [result.update(self.key_add)]
        return result

    def _setup_ui(self):
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
        self.widgets = defaultdict(list)
        for key, val in self.param.items():
            widget = None
            param_type = None
            if "array" in val[0] or "QtWidget" in val[0]:
                # skip input that could be an array because its too hard to find a way to handle them
                print("skipping : ", val[0])
                continue
            elif "str" in val[0]:
                default_val = val[1] if val[1] is not None else key
                widget = QLineEdit()
                widget.setPlaceholderText(self._set_default(widget, default_val))
                param_type = "str"
            elif "int" in val[0] or "scalar" in val[0] or "float" in val[0]:
                widget = self._create_int_float(val, True if "float" in val[0] else False)
                param_type = "int"

            elif "bool" in val[0]:
                default_val = val[1] if val[1] is not None else False
                widget = QCheckBox()
                widget.setChecked(self._set_default(widget, default_val))
                param_type = "bool"
            elif "iterable" in val[0]:
                iter_ran = int(''.join(x for x in val[0] if x.isdigit()))
                widget = QtWidgets.QWidget()
                lay = QVBoxLayout()
                for el in range(iter_ran):
                    lay.addWidget(self._create_int_float(val))
                widget.setLayout(lay)
                param_type = "iterable_" + str(iter_ran)

            else:
                print("TODO : Implement : ", val[0])
                continue
            none_possible = False
            if "None" in val[0]:
                none_possible = True
            widget.setToolTip(val[2])
            self.widgets[param_type].append([key, widget, none_possible])
        self._format_layout()

    def _create_int_float(self, val, is_float=False):
        default_val = val[1] if val[1] is not None else 0
        if is_float:
            widget = QDoubleSpinBox()
        else:
            widget = QSpinBox()
        widget.setValue(self._set_default(widget, default_val))
        widget.setMinimum(-1000)
        widget.setMaximum(1000)
        return widget

    def _save(self):
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    self.result[key] = widget.isChecked()
                elif param_type == "int":
                    tmp = widget.value()
                    if none_possible and tmp == 0:
                        tmp = None
                    self.result[key] = tmp
                elif "iterable" in param_type:
                    val_ls = []
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        val_ls.append(self.sub_ls[widget][el].value())
                    self.result[key] = val_ls
                else:
                    self.result[key] = widget.text()
        # print(self.result)
        self.accept()

    def get_result(self):
        return self.result

    def _set_default(self, widget, default_val):
        self.default[widget] = default_val
        return default_val

    def _restore_default(self):
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    widget.setChecked(self.default[widget])
                elif param_type == "int":
                    widget.setValue(self.default[widget])
                elif "iterable" in param_type:
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        self.sub_ls[widget][el].setValue(0)
                else:
                    widget.clear()
                    widget.setPlaceholderText(self.default[widget])

    def _format_layout(self):
        # Create layout and add widgets
        all_widget = []
        self.sub_ls = defaultdict(list)
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    widget.setFixedWidth(20)
                if param_type != "bool":
                    widget.setFixedWidth(100)
                widget.setFixedHeight(30)
                if "iterable" in param_type:
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        sub_widget = widget.layout().itemAt(el).widget()
                        self.sub_ls[widget].append(sub_widget)
                        sub_widget.setFixedWidth(100)
                        sub_widget.setFixedHeight(30)
                        all_widget.append((key.replace("_", " ").capitalize() + " " + str(el), sub_widget))
                else:
                    all_widget.append((key.replace("_", " ").capitalize(), widget))
                # self.layout.addRow(key.replace("_", " ").capitalize(), widget)
        layout = QGridLayout()

        self._create_colums(all_widget, layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save |
                                     QDialogButtonBox.Cancel |
                                     QDialogButtonBox.RestoreDefaults)
        buttonBox.accepted.connect(self._save)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self._restore_default)
        layout.addWidget(buttonBox, 1, 0, 1, len(all_widget) // self.items_per_column + 1, Qt.AlignRight)
        self.setLayout(layout)
        self.setFixedSize(self.minimumWidth(), self.minimumHeight())

    def _create_colums(self, widget_list, vert_layout, n=0):
        tmp = QtWidgets.QWidget()
        layout = QFormLayout()
        for name, widget in widget_list[0 + self.items_per_column *
                                        n:self.items_per_column + self.items_per_column * n]:
            layout.addRow(name, widget)
        tmp.setLayout(layout)
        tmp.setFixedWidth(110 + layout.itemAt(0, QFormLayout.FieldRole).geometry().width())
        vert_layout.addWidget(tmp, 0, n)
        if self.items_per_column * (n + 1) >= len(widget_list):
            return
        self._create_colums(widget_list, vert_layout, n=n + 1)
