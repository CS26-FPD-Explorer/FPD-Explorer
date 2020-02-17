# Standard Library
import inspect
from inspect import signature
from collections import defaultdict

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QWidget,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QFormLayout,
    QGridLayout,
    QVBoxLayout,
    QDoubleSpinBox,
    QDialogButtonBox
)

# FPD Explorer
from . import config_handler as config


class UI_Generator(QtWidgets.QDialog):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    application_window : QApplication
        The parent in which the tab should be rendered
    fnct : function
        The function object for which we want to create the input box
            Parameters
    items_per_column : int, optional
        Number of widgets per colum, by default 10
    key_ignore : list, optional
        List of variable names to be removed from the GUI, by default None
    key_add : dict , optional
        Dict with variable name as a key and a list composed of type, default value and description,
        by default None

    """

    def __init__(self, application_window, fnct, items_per_column=10, key_ignore=None, key_add=None):
        super(UI_Generator, self).__init__()
        self.application_window = application_window
        self.key_ignore = key_ignore
        self.key_add = key_add
        self.items_per_column = items_per_column
        self.default = {}
        # This must always be last and in that order
        self.fnct = fnct.__name__
        self.config_val = config.get_dict(self.fnct)
        self.param = self._get_param(fnct)
        self._setup_ui()
        self.setWindowFlags((self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint) & ~Qt.WindowContextHelpButtonHint)

    def _get_param(self, fnct) -> dict:
        """
        Get the paramaters based of a given function

        Uses the docstring and parses it. Must respect numpy style docstring to parse correctly
        Also uses the function siganture to get default

        Parameters
        ----------
        fnct : fnct
            The function you want to get the parameter of

        Returns
        ----------
        result : dict
            A dict with the variable name as a key and the default value and description as item
        """
        sig = signature(fnct)
        doc = fnct.__doc__
        result = {}
        # result is a dict with the variable name as key and a list composed of type, default value, description
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
            result.update(self.key_add)

        return result

    def _setup_ui(self):
        """
        Creates the UI. Assumes the parameter list has already been defined
        self.widgets is a dictionary with the type as key and a list of widgets as val

        the list of widgets is compossed of a list compossed of key, widget, None value possible
        {
            type:[
                [key, widget, bool],
            ],
        }
        """
        self.result = {}
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
                tmp_val = self.config_val.get(key, None)
                if tmp_val is not None:
                    widget.setText(tmp_val)
                param_type = "str"
            elif "int" in val[0] or "scalar" in val[0] or "float" in val[0]:
                widget = self._create_int_float(val, True if "float" in val[0] else False, key=key)
                param_type = "int"
            elif "bool" in val[0]:
                default_val = val[1] if val[1] is not None else False
                widget = QCheckBox()
                widget.setChecked(self._set_default(widget, default_val))
                tmp_val = self.config_val.get(key, None)
                if tmp_val is not None:
                    widget.setChecked(tmp_val)
                param_type = "bool"
            elif "iterable" in val[0]:
                iter_ran = int(''.join(x for x in val[0] if x.isdigit()))
                widget = QWidget()
                lay = QVBoxLayout()
                unpack = False
                if isinstance(val[1], tuple) or isinstance(val[1], list):
                    # Expect to have as many value in the tuple as there is required by the iterable
                    unpack = True
                for el in range(iter_ran):
                    new_val = list(val)
                    if unpack:
                        new_val[1] = val[1][el]
                    lay.addWidget(self._create_int_float(new_val, key=key + '_' + str(el)))
                widget.setLayout(lay)
                param_type = "iterable_" + str(iter_ran)
            elif "multipleinput" in val[0]:
                param_type = "multipleinput"
                widget = QComboBox()
                for idx, el in enumerate(val[1]):
                    widget.addItem(el[0])
                    widget.setItemData(idx, el[1])
            else:
                print("TODO : Implement : ", val[0])
                continue
            none_possible = False
            if "None" in val[0]:
                none_possible = True
            widget.setToolTip(val[2])
            self.widgets[param_type].append([key, widget, none_possible])
        self._format_layout()

    def _create_int_float(self, val, is_float: bool = False, key: str = None) -> QWidget:
        """
        Creates the widget for integer or float

        Parameters
        ----------
        val : list
            list of type, default value, description
        is_float : bool, optional
            is the value suposed to be a float, by default False
        key : str, optional
            The variable name, by default None

        Returns
        -------
        QWidget
            The given widget correctly set up
        """
        default_val = val[1] if val[1] is not None else 0
        if is_float:
            widget = QDoubleSpinBox()
        else:
            widget = QSpinBox()
        # Needed to return to default if they ever want it
        widget.setMinimum(-1000)
        widget.setMaximum(1000)
        widget.setValue(self._set_default(widget, default_val))
        tmp_val = self.config_val.get(key, None)
        if isinstance(tmp_val, str):
            if 'None' not in tmp_val:
                widget.setValue(float(tmp_val))
        elif tmp_val is not None:
            widget.setValue(float(tmp_val))
        return widget

    def _save(self):
        """
        Save is the function called to get the parameter out of the widget and save them to the file
        It saves everything inside self.result
        It also creates a saved_result dict to save to file as iterable are not handled otherwise
        """
        saved_result = {}
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                # Use skip if there is no need to save to file as it is
                skip = False
                if param_type == "bool":
                    val = widget.isChecked()
                elif param_type == "int":
                    val = widget.value()
                    if none_possible and (val == 0 or val == 0.0):
                        val = None
                elif "iterable" in param_type:
                    val = []
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        value = self.sub_ls[widget][el].value()
                        val.append(value)
                        saved_result[key + "_" + str(el)] = value
                    skip = True
                elif param_type == "multipleinput":
                    val = widget.itemData(widget.currentIndex())
                    skip = True
                else:
                    val = widget.text()
                self.result[key] = val
                if not skip:
                    if param_type != "bool":
                        val = str(val)
                    saved_result[key] = val
        config.add_config({self.fnct: saved_result})
        self.accept()

    def get_result(self) -> dict:
        """
        Returns the value collected by the widget

        Returns
        -------
        dict
            Dict composed of variable name as key and the value entered by the user
        """
        return self.result

    def _set_default(self, widget: QWidget, default_val: object) -> object:
        """
        Saves the default value in a dict used to restore to default

        Parameters
        ----------
        widget : QWidget
            The widget that should have this default value
        default_val : object
            The default value

        Returns
        -------
        object
            returns the input
        """
        self.default[widget] = default_val
        return default_val

    def _restore_default(self):
        """
        Restores all the widget to their default value
        """
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                if param_type == "bool":
                    widget.setChecked(self.default[widget])
                elif param_type == "int":
                    widget.setValue(self.default[widget])
                elif "iterable" in param_type:
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        sub_widget = self.sub_ls[widget][el]
                        self.sub_ls[widget][el].setValue(self.default[sub_widget])
                elif param_type == "multipleinput":
                    widget.setCurrentIndex(0)
                else:
                    widget.clear()
                    widget.setPlaceholderText(self.default[widget])

    def _format_layout(self):
        """
        Creates the layout and organize it based on the list of widgets
        """
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
                        # Loop for all children and add them as single child
                        sub_widget = widget.layout().itemAt(el).widget()
                        self.sub_ls[widget].append(sub_widget)
                        sub_widget.setFixedWidth(100)
                        sub_widget.setFixedHeight(30)
                        all_widget.append((key.replace("_", " ").capitalize() + " " + str(el), sub_widget, param_type))
                else:
                    all_widget.append((key.replace("_", " ").capitalize(), widget, param_type))
                # self.layout.addRow(key.replace("_", " ").capitalize(), widget)
        layout = QGridLayout()
        all_widget.sort(key=lambda x: x[2], reverse=True)
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

    def _create_colums(self, widget_list: list, grid_layout: QtWidgets.QGridLayout, n=0):
        """
        Recursively add items to a column
        The number of items per colum depends on self.items_per_column

        Parameters
        ----------
        widget_list : list
            list of all widgets that need to be added
        grid_layout : QtWidgets.QGridLayout
            the grid layout where the widgets must be added
        n : int, optional
            Used for recursion to keep track on how many items have already been added, by default 0
        """
        tmp = QWidget()
        layout = QFormLayout()
        for name, widget, _ in widget_list[0 + self.items_per_column *
                                           n:self.items_per_column + self.items_per_column * n]:
            layout.addRow(name, widget)
        tmp.setLayout(layout)
        tmp.setFixedWidth(110 + layout.itemAt(0, QFormLayout.FieldRole).geometry().width())
        grid_layout.addWidget(tmp, 0, n)
        if self.items_per_column * (n + 1) >= len(widget_list):
            return
        self._create_colums(widget_list, grid_layout, n=n + 1)
