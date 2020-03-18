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
import inspect
from inspect import signature
from collections import defaultdict

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Slot
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
from .. import config_handler as config


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
        if fnct is not None:
            self.fnct = fnct.__name__
            self.config_val = config.get_dict(self.fnct)
            self.param = self._get_param(fnct)
        else:
            self.fnct = None
            self.config_val = {}
            self.param = self.handle_key_edits({})
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
        if doc:
            # result is a dict with the variable name as key and a list composed of type, default value, description
            param = doc.split('Parameters')[1].replace(',', '').replace(
                '-', '').split("Return")[0].split("Attributes")[0].split("Notes")[0].split('\n')
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
        return self.handle_key_edits(result)

    def handle_key_edits(self, result):
        if self.key_ignore is not None:
            [result.pop(x, None) for x in self.key_ignore]
        if self.key_add is not None:
            for key, el in self.key_add.items():
                # Remove all key already present in the dict so no key gets processed twice
                if result.get(key, None) is not None:
                    result.pop(key)
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
        self.toggle_widget = defaultdict(list)
        for key, val in self.param.items():
            widget = None
            param_type = None
            if "array" in val[0] or "QtWidget" in val[0]:
                # skip input that could be an array because its too hard to find a way to handle them
                # print("skipping : ", val[0])
                continue
            if "cmap" in val[0] or "colormap" in val[0].lower():
                param_type = "multipleinput"
                widget = QComboBox()
                for el in self.application_window.cmaps.values():
                    for cmaps in el:
                        widget.addItem(cmaps)

            elif "str" in val[0]:
                widget = QLineEdit()
                if val[1] is None:
                    widget.setPlaceholderText(self._set_default(widget, key))
                else:
                    widget.setText(self._set_default(widget, val[1]))
                tmp_val = self.config_val.get(key, None)
                if tmp_val is not None:
                    widget.setText(tmp_val)
                param_type = "str"
            elif "tuple" in val[0]:
                param_type, widget = self._handle_iterable(val, key)
            elif "scalar" in val[0] or "float" in val[0]:
                widget = self._create_int_float(val, is_float=True, key=key)
                param_type = "int"
            elif "int" in val[0]:
                widget = self._create_int_float(val, key=key)
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
                # Repetition needed because int should be prioritized over iterable and tuple over scalar
                param_type, widget = self._handle_iterable(val, key)
            elif "multipleinput" in val[0]:
                param_type = "multipleinput"
                widget = QComboBox()
                for idx, el in enumerate(val[1]):
                    widget.addItem(el[0])
                    widget.setItemData(idx, el[1])
                tmp_val = self.config_val.get(key, None)
                if tmp_val is not None:
                    # Float needed because otherwise Python throws a fit
                    widget.setCurrentIndex(int(float(tmp_val)))
                else:
                    widget.setCurrentIndex(0)
            elif "togglevalue" in val[0]:
                param_type = "togglevalue"
                widget = QCheckBox()
                widget.setChecked(False)
                widget.stateChanged.connect(self._handle_togglevalue)
                sub_param_type, new_widget = self._handle_iterable(val[1], key)
                self.toggle_widget[key].extend([sub_param_type, new_widget])
                if val[1][1] is None:
                    val[0] += "None"
            else:
                # print("TODO : Implement : ", val[0])
                continue
            none_possible = False
            if "None" in val[0]:
                none_possible = True
            widget.setToolTip(val[2])
            self.widgets[param_type].append([key, widget, none_possible])
        self._format_layout()

    def _handle_iterable(self, val, key):
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
            lay.addWidget(self._create_int_float(new_val, key=key + '_' + str(el), is_float=True))
        widget.setLayout(lay)
        param_type = "iterable_" + str(iter_ran)
        return param_type, widget

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
        widget.setMinimum(-1000)
        widget.setMaximum(1000)
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
        widget.setToolTip(val[2])
        return widget

    @Slot(int)
    def _handle_togglevalue(self, state: int):
        caller = self.sender()
        if state == 2:
            flatten_widget = []
            already_placed = 0
            correct_key = None
            for key, widget, none_possible in self.widgets["togglevalue"]:
                if widget == caller:
                    correct_key = key
                    out = self.toggle_widget[key]
                    # Handle unpacking with variable amount
                    param_type = out[0]
                    sub_widget = out[1]
                    self._layout_iterable(key, sub_widget, param_type, flatten_widget)
            self.toggle_widget[correct_key].append(list(flatten_widget))
            for name, widget, _ in flatten_widget[:self.number_space]:
                self.last_colums[self.last_n].layout().addRow(name, widget)
                already_placed += 1
            self.number_space -= already_placed
            del flatten_widget[:already_placed]
            while len(flatten_widget) > 0:
                self.last_n += 1
                self.last_colums.append(self.add_forms(flatten_widget, self.grid_layout,
                                                       0, self.items_per_column, self.last_n))
                self.number_space = self.items_per_column - len(flatten_widget)
                del flatten_widget[:self.items_per_column]

        else:
            self._delete_toggle_value(caller)

    def _delete_toggle_value(self, caller):
        for key, widget, none_possible in self.widgets["togglevalue"]:
            if widget == caller:
                lay = self.toggle_widget[key][1].layout()
                param_type, sub_widget, widget_ls = self.toggle_widget[key]
                for name, sub_sub_widget, param_type in widget_ls:
                    sub_sub_widget.parent().layout().labelForField(sub_sub_widget).deleteLater()
                    # sub_sub_widget.deleteLater()
                    lay.addWidget(sub_sub_widget)
                    # print(self.number_space, self.last_n, self.last_colums)
                    if self.number_space != 10:
                        self.number_space += 1
                    else:
                        self.number_space = 1
                        self.grid_layout.removeWidget(self.last_colums[self.last_n])
                        self.last_colums[self.last_n].deleteLater()
                        del self.last_colums[self.last_n]
                        self.last_n -= 1
                self.setFixedSize(self.min_size[0], self.min_size[1])
                del self.toggle_widget[key][2]

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
                    none_list = False
                    iter_ran = int(param_type.split("_")[1])
                    for el in range(iter_ran):
                        value = self.sub_ls[widget][el].value()
                        val.append(value)
                        if none_possible and (value == 0 or value == 0.0):
                            none_list = True
                            value = None
                        saved_result[key + "_" + str(el)] = str(value)
                    if none_list:
                        val = None
                    skip = True
                elif param_type == "multipleinput":
                    val = widget.itemData(widget.currentIndex())
                    # Repeated code because val should be the index and not the data
                    saved_result[key] = str(widget.currentIndex())
                    skip = True
                elif param_type == "togglevalue":
                    if not widget.isChecked():
                        continue
                    val = []
                    none_list = False
                    counter = 0
                    for name, sub_sub_widget, _ in self.toggle_widget[key][2]:
                        value = sub_sub_widget.value()
                        val.append(value)
                        if none_possible and (value == 0 or value == 0.0):
                            none_list = True
                            value = None
                        saved_result[name + "_" + str(counter)] = str(value)
                        counter += 1
                    if none_list:
                        val = None
                    skip = True

                else:
                    val = widget.text()
                    if none_possible and val == '':
                        val = None

                self.result[key] = val
                if not skip:
                    if param_type != "bool":
                        val = str(val)
                    saved_result[key] = val
        if self.fnct is not None:
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
                elif param_type == "togglevalue":
                    if widget.isChecked():
                        self._delete_toggle_value(widget)
                    widget.setChecked(False)
                else:
                    widget.clear()
                    widget.setPlaceholderText(self.default[widget])

    def _layout_iterable(self, key, widget, param_type, append_ls):
        iter_ran = int(param_type.split("_")[1])
        for idx in range(iter_ran):
            sub_widget = widget.layout().itemAt(idx).widget()
            self.sub_ls[widget].append(sub_widget)
            sub_widget.setFixedWidth(100)
            sub_widget.setFixedHeight(30)
            append_ls.append((key.replace("_", " ").capitalize() + " " + str(idx), sub_widget, param_type))

    def _format_layout(self):
        """
        Creates the layout and organize it based on the list of widgets
        """
        # Create layout and add widgets
        all_widget = []
        self.sub_ls = defaultdict(list)
        for param_type, widgets in self.widgets.items():
            for key, widget, none_possible in widgets:
                # if param_type == "bool":
                # widget.setFixedWidth(20)
                # if param_type != "bool":
                widget.setFixedWidth(100)
                widget.setFixedHeight(30)
                if "iterable" in param_type:
                    # Loop for all children and add them as single child
                    self._layout_iterable(key, widget, param_type, all_widget)
                else:
                    all_widget.append((key.replace("_", " ").capitalize(), widget, param_type))
                # self.layout.addRow(key.replace("_", " ").capitalize(), widget)
        self.grid_layout = QGridLayout()
        all_widget.sort(key=lambda x: x[2], reverse=True)
        self.last_colums = []
        self.number_space, self.last_n = self._create_colums(all_widget, self.grid_layout)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel |
                                     QDialogButtonBox.RestoreDefaults)
        buttonBox.accepted.connect(self._save)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self._restore_default)
        self.grid_layout.addWidget(buttonBox, 1, 0, 1, len(all_widget) // self.items_per_column + 1, Qt.AlignRight)
        self.setLayout(self.grid_layout)
        self.min_size = (self.minimumWidth(), self.minimumHeight())
        self.setFixedSize(self.min_size[0], self.min_size[1])

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
        slice_bottom = 0 + self.items_per_column * n
        slice_top = self.items_per_column + self.items_per_column * n

        layout = self.add_forms(widget_list, grid_layout, slice_bottom, slice_top, n)
        self.last_colums.append(layout)
        if self.items_per_column * (n + 1) >= len(widget_list):
            return self.items_per_column - len(widget_list[slice_bottom:slice_top]), n
        return self._create_colums(widget_list, grid_layout, n=n + 1)

    def add_forms(self, widget_list: list, grid_layout: QtWidgets.QGridLayout, slice_bottom: int, slice_top: int, n=0):
        tmp = QWidget()
        layout = QFormLayout()
        for name, widget, _ in widget_list[slice_bottom:slice_top]:
            layout.addRow(name, widget)
        tmp.setLayout(layout)
        tmp.setFixedWidth(110 + layout.itemAt(0, QFormLayout.FieldRole).geometry().width())
        grid_layout.addWidget(tmp, 0, n)
        return tmp
