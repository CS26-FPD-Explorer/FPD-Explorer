# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadingbox.ui',
# licensing of 'loadingbox.ui' applies.
#
# Created: Mon Nov 11 18:30:18 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoadingBox(object):
    def setupUi(self, LoadingBox):
        LoadingBox.setObjectName("LoadingBox")
        LoadingBox.resize(400, 114)
        LoadingBox.setMinimumSize(QtCore.QSize(400, 114))
        LoadingBox.setMaximumSize(QtCore.QSize(400, 114))
        self.gridLayout = QtWidgets.QGridLayout(LoadingBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.recipProgress = QtWidgets.QProgressBar(LoadingBox)
        self.recipProgress.setProperty("value", 24)
        self.recipProgress.setObjectName("recipProgress")
        self.gridLayout_6.addWidget(self.recipProgress, 1, 1, 1, 1)
        self.realProgress = QtWidgets.QProgressBar(LoadingBox)
        self.realProgress.setProperty("value", 24)
        self.realProgress.setObjectName("realProgress")
        self.gridLayout_6.addWidget(self.realProgress, 0, 1, 1, 1)
        self.recipButton = QtWidgets.QRadioButton(LoadingBox)
        self.recipButton.setObjectName("recipButton")
        self.spaceGroup = QtWidgets.QButtonGroup(LoadingBox)
        self.spaceGroup.setObjectName("spaceGroup")
        self.spaceGroup.addButton(self.recipButton)
        self.gridLayout_6.addWidget(self.recipButton, 1, 0, 1, 1)
        self.realButton = QtWidgets.QRadioButton(LoadingBox)
        self.realButton.setChecked(True)
        self.realButton.setObjectName("realButton")
        self.spaceGroup.addButton(self.realButton)
        self.gridLayout_6.addWidget(self.realButton, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.restoreButton = QtWidgets.QPushButton(LoadingBox)
        self.restoreButton.setObjectName("restoreButton")
        self.horizontalLayout.addWidget(self.restoreButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoadingBox)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(LoadingBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LoadingBox.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LoadingBox.reject)
        QtCore.QObject.connect(self.restoreButton, QtCore.SIGNAL("clicked()"), self.realButton.click)
        QtCore.QObject.connect(self.realButton, QtCore.SIGNAL("clicked()"), LoadingBox.change_button)
        QtCore.QObject.connect(self.recipButton, QtCore.SIGNAL("clicked()"), LoadingBox.change_button)
        QtCore.QMetaObject.connectSlotsByName(LoadingBox)

    def retranslateUi(self, LoadingBox):
        LoadingBox.setWindowTitle(QtWidgets.QApplication.translate("LoadingBox", "Dialog", None, -1))
        self.recipButton.setText(QtWidgets.QApplication.translate("LoadingBox", "Sum Recip Space", None, -1))
        self.realButton.setText(QtWidgets.QApplication.translate("LoadingBox", "Sum Real Space", None, -1))
        self.restoreButton.setText(QtWidgets.QApplication.translate("LoadingBox", "Restore Default", None, -1))

