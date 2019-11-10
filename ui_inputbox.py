# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputbox.ui',
# licensing of 'inputbox.ui' applies.
#
# Created: Sun Nov 10 01:24:33 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_InputBox(object):
    def setupUi(self, InputBox):
        InputBox.setObjectName("InputBox")
        InputBox.resize(400, 150)
        InputBox.setMinimumSize(QtCore.QSize(400, 150))
        InputBox.setMaximumSize(QtCore.QSize(400, 150))
        self.gridLayout_2 = QtWidgets.QGridLayout(InputBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setCursor(QtCore.Qt.ArrowCursor)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setCursor(QtCore.Qt.ArrowCursor)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(InputBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 1, 2, 2)
        self.Xsize = QtWidgets.QSpinBox(InputBox)
        self.Xsize.setWrapping(True)
        self.Xsize.setMinimum(2)
        self.Xsize.setMaximum(8192)
        self.Xsize.setSingleStep(1)
        self.Xsize.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Xsize.setProperty("value", 256)
        self.Xsize.setDisplayIntegerBase(10)
        self.Xsize.setObjectName("Xsize")
        self.gridLayout_2.addWidget(self.Xsize, 0, 1, 1, 2)
        self.Ysize = QtWidgets.QSpinBox(InputBox)
        self.Ysize.setMinimum(2)
        self.Ysize.setMaximum(8192)
        self.Ysize.setSingleStep(2)
        self.Ysize.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Ysize.setProperty("value", 256)
        self.Ysize.setObjectName("Ysize")
        self.gridLayout_2.addWidget(self.Ysize, 1, 1, 1, 2)

        self.retranslateUi(InputBox)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), InputBox.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), InputBox.reject)
        QtCore.QMetaObject.connectSlotsByName(InputBox)

    def retranslateUi(self, InputBox):
        InputBox.setWindowTitle(QtWidgets.QApplication.translate("InputBox", "Dialog", None, -1))
        self.lineEdit_3.setText(QtWidgets.QApplication.translate("InputBox", "Y read size", None, -1))
        self.lineEdit_4.setText(QtWidgets.QApplication.translate("InputBox", "X read size", None, -1))

