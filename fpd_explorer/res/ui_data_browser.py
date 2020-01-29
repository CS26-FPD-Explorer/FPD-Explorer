# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fpd_explorer\res\data_browser.ui',
# licensing of '.\fpd_explorer\res\data_browser.ui' applies.
#
# Created: Fri Jan 24 21:15:22 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DataBrowser(object):
    def setupUi(self, DataBrowser):
        DataBrowser.setObjectName("DataBrowser")
        DataBrowser.resize(1087, 636)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DataBrowser)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.navigationWidget = QtWidgets.QWidget(DataBrowser)
        self.navigationWidget.setObjectName("navigationWidget")
        self.navigationLayout = QtWidgets.QGridLayout(self.navigationWidget)
        self.navigationLayout.setContentsMargins(0, 0, 0, 0)
        self.navigationLayout.setObjectName("navigationLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.navX = QtWidgets.QSpinBox(self.navigationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navX.sizePolicy().hasHeightForWidth())
        self.navX.setSizePolicy(sizePolicy)
        self.navX.setWrapping(True)
        self.navX.setMinimum(1)
        self.navX.setProperty("value", 2)
        self.navX.setObjectName("navX")
        self.gridLayout_6.addWidget(self.navX, 0, 1, 1, 1)
        self.navY = QtWidgets.QSpinBox(self.navigationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navY.sizePolicy().hasHeightForWidth())
        self.navY.setSizePolicy(sizePolicy)
        self.navY.setWrapping(True)
        self.navY.setFrame(True)
        self.navY.setMinimum(1)
        self.navY.setProperty("value", 2)
        self.navY.setObjectName("navY")
        self.gridLayout_6.addWidget(self.navY, 0, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.navigationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.navigationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_6.addWidget(self.lineEdit_2, 0, 2, 1, 1)
        self.navigationLayout.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.navCanvas = MyMplCanvas(self.navigationWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navCanvas.sizePolicy().hasHeightForWidth())
        self.navCanvas.setSizePolicy(sizePolicy)
        self.navCanvas.setObjectName("navCanvas")
        self.gridLayout = QtWidgets.QGridLayout(self.navCanvas)
        self.gridLayout.setContentsMargins(20, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.navigationLayout.addWidget(self.navCanvas, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.navigationWidget)
        self.diffractionWidget = QtWidgets.QWidget(DataBrowser)
        self.diffractionWidget.setObjectName("diffractionWidget")
        self.diffractionLayout = QtWidgets.QGridLayout(self.diffractionWidget)
        self.diffractionLayout.setContentsMargins(0, 0, 0, 0)
        self.diffractionLayout.setObjectName("diffractionLayout")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.diffractionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_7.addWidget(self.lineEdit_4, 0, 0, 1, 1)
        self.colorMap = QtWidgets.QComboBox(self.diffractionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorMap.sizePolicy().hasHeightForWidth())
        self.colorMap.setSizePolicy(sizePolicy)
        self.colorMap.setCurrentText("")
        self.colorMap.setObjectName("colorMap")
        self.gridLayout_7.addWidget(self.colorMap, 0, 1, 1, 1)
        self.diffractionLayout.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.diffCanvas = MyMplCanvas(self.diffractionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffCanvas.sizePolicy().hasHeightForWidth())
        self.diffCanvas.setSizePolicy(sizePolicy)
        self.diffCanvas.setObjectName("diffCanvas")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.diffCanvas)
        self.gridLayout_2.setContentsMargins(20, -1, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.diffractionLayout.addWidget(self.diffCanvas, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.diffractionWidget)

        self.retranslateUi(DataBrowser)
        QtCore.QObject.connect(self.navY, QtCore.SIGNAL("valueChanged(int)"), DataBrowser.update_rect)
        QtCore.QObject.connect(self.navX, QtCore.SIGNAL("valueChanged(int)"), DataBrowser.update_rect)
        QtCore.QObject.connect(self.colorMap, QtCore.SIGNAL("currentTextChanged(QString)"), DataBrowser.update_color_map)
        QtCore.QMetaObject.connectSlotsByName(DataBrowser)

    def retranslateUi(self, DataBrowser):
        DataBrowser.setWindowTitle(QtWidgets.QApplication.translate("DataBrowser", "Form", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("DataBrowser", "X size", None, -1))
        self.lineEdit_2.setText(QtWidgets.QApplication.translate("DataBrowser", "Y size", None, -1))
        self.lineEdit_4.setText(QtWidgets.QApplication.translate("DataBrowser", "Color Map", None, -1))

from fpd_explorer.custom_widgets import MyMplCanvas
