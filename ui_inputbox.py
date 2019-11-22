# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputbox.ui',
# licensing of 'inputbox.ui' applies.
#
# Created: Fri Nov 22 23:01:39 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_InputBox(object):
    def setupUi(self, InputBox):
        InputBox.setObjectName("InputBox")
        InputBox.resize(400, 114)
        InputBox.setMinimumSize(QtCore.QSize(400, 114))
        InputBox.setMaximumSize(QtCore.QSize(400, 114))
        self.gridLayout = QtWidgets.QGridLayout(InputBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.Ysize = QtWidgets.QSpinBox(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Ysize.sizePolicy().hasHeightForWidth())
        self.Ysize.setSizePolicy(sizePolicy)
        self.Ysize.setMinimum(1)
        self.Ysize.setMaximum(13)
        self.Ysize.setSingleStep(1)
        self.Ysize.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.Ysize.setProperty("value", 8)
        self.Ysize.setObjectName("Ysize")
        self.gridLayout_6.addWidget(self.Ysize, 1, 1, 1, 1)
        self.Xsize = QtWidgets.QSpinBox(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Xsize.sizePolicy().hasHeightForWidth())
        self.Xsize.setSizePolicy(sizePolicy)
        self.Xsize.setWrapping(True)
        self.Xsize.setSuffix("")
        self.Xsize.setMinimum(1)
        self.Xsize.setMaximum(13)
        self.Xsize.setSingleStep(1)
        self.Xsize.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.Xsize.setProperty("value", 8)
        self.Xsize.setDisplayIntegerBase(10)
        self.Xsize.setObjectName("Xsize")
        self.gridLayout_6.addWidget(self.Xsize, 0, 1, 1, 1)
        self.Ytext = QtWidgets.QLineEdit(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Ytext.sizePolicy().hasHeightForWidth())
        self.Ytext.setSizePolicy(sizePolicy)
        self.Ytext.setCursor(QtCore.Qt.ArrowCursor)
        self.Ytext.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Ytext.setReadOnly(True)
        self.Ytext.setObjectName("Ytext")
        self.gridLayout_6.addWidget(self.Ytext, 1, 0, 1, 1)
        self.Xvalue = QtWidgets.QLineEdit(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Xvalue.sizePolicy().hasHeightForWidth())
        self.Xvalue.setSizePolicy(sizePolicy)
        self.Xvalue.setCursor(QtCore.Qt.ArrowCursor)
        self.Xvalue.setReadOnly(True)
        self.Xvalue.setObjectName("Xvalue")
        self.gridLayout_6.addWidget(self.Xvalue, 0, 2, 1, 1)
        self.Xtext = QtWidgets.QLineEdit(InputBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Xtext.sizePolicy().hasHeightForWidth())
        self.Xtext.setSizePolicy(sizePolicy)
        self.Xtext.setObjectName("Xtext")
        self.gridLayout_6.addWidget(self.Xtext, 0, 0, 1, 1)
        self.Yvalue = QtWidgets.QLineEdit(InputBox)
        self.Yvalue.setObjectName("Yvalue")
        self.gridLayout_6.addWidget(self.Yvalue, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.restoreButton = QtWidgets.QPushButton(InputBox)
        self.restoreButton.setObjectName("restoreButton")
        self.horizontalLayout.addWidget(self.restoreButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(InputBox)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(InputBox)
        QtCore.QObject.connect(self.Xsize, QtCore.SIGNAL("valueChanged(int)"), InputBox.update_value)
        QtCore.QObject.connect(self.Ysize, QtCore.SIGNAL("valueChanged(int)"), InputBox.update_value)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), InputBox.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), InputBox.reject)
        QtCore.QObject.connect(self.restoreButton, QtCore.SIGNAL("clicked()"), InputBox.restore_default)
        QtCore.QMetaObject.connectSlotsByName(InputBox)

    def retranslateUi(self, InputBox):
        InputBox.setWindowTitle(QtWidgets.QApplication.translate("InputBox", "Dialog", None, -1))
        self.Ysize.setPrefix(QtWidgets.QApplication.translate("InputBox", "2^", None, -1))
        self.Xsize.setPrefix(QtWidgets.QApplication.translate("InputBox", "2^", None, -1))
        self.Ytext.setText(QtWidgets.QApplication.translate("InputBox", "Y read size", None, -1))
        self.Xvalue.setText(QtWidgets.QApplication.translate("InputBox", "= 256", None, -1))
        self.Xtext.setText(QtWidgets.QApplication.translate("InputBox", "X read size", None, -1))
        self.Yvalue.setText(QtWidgets.QApplication.translate("InputBox", "= 256", None, -1))
        self.restoreButton.setText(QtWidgets.QApplication.translate("InputBox", "Restore Default", None, -1))

