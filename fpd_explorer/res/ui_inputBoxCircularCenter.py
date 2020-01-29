# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fpd_explorer\res\inputBoxCircularCenter.ui',
# licensing of '.\fpd_explorer\res\inputBoxCircularCenter.ui' applies.
#
# Created: Fri Jan 24 21:15:24 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CircularCenterInput(object):
    def setupUi(self, CircularCenterInput):
        CircularCenterInput.setObjectName("CircularCenterInput")
        CircularCenterInput.resize(429, 178)
        self.verticalLayout = QtWidgets.QVBoxLayout(CircularCenterInput)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rmms2nd = QtWidgets.QSpinBox(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rmms2nd.sizePolicy().hasHeightForWidth())
        self.rmms2nd.setSizePolicy(sizePolicy)
        self.rmms2nd.setPrefix("")
        self.rmms2nd.setMinimum(0)
        self.rmms2nd.setMaximum(10000)
        self.rmms2nd.setSingleStep(1)
        self.rmms2nd.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.rmms2nd.setProperty("value", 60)
        self.rmms2nd.setObjectName("rmms2nd")
        self.gridLayout.addWidget(self.rmms2nd, 1, 1, 1, 1)
        self.rmms3rd = QtWidgets.QSpinBox(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rmms3rd.sizePolicy().hasHeightForWidth())
        self.rmms3rd.setSizePolicy(sizePolicy)
        self.rmms3rd.setPrefix("")
        self.rmms3rd.setMinimum(0)
        self.rmms3rd.setMaximum(10000)
        self.rmms3rd.setSingleStep(1)
        self.rmms3rd.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.rmms3rd.setProperty("value", 1)
        self.rmms3rd.setObjectName("rmms3rd")
        self.gridLayout.addWidget(self.rmms3rd, 2, 1, 1, 1)
        self.Xtext = QtWidgets.QLineEdit(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Xtext.sizePolicy().hasHeightForWidth())
        self.Xtext.setSizePolicy(sizePolicy)
        self.Xtext.setCursor(QtCore.Qt.ArrowCursor)
        self.Xtext.setReadOnly(True)
        self.Xtext.setObjectName("Xtext")
        self.gridLayout.addWidget(self.Xtext, 0, 0, 1, 1)
        self.rmms1st = QtWidgets.QSpinBox(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rmms1st.sizePolicy().hasHeightForWidth())
        self.rmms1st.setSizePolicy(sizePolicy)
        self.rmms1st.setWrapping(True)
        self.rmms1st.setSuffix("")
        self.rmms1st.setPrefix("")
        self.rmms1st.setMinimum(0)
        self.rmms1st.setMaximum(1000)
        self.rmms1st.setSingleStep(1)
        self.rmms1st.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.rmms1st.setProperty("value", 10)
        self.rmms1st.setDisplayIntegerBase(10)
        self.rmms1st.setObjectName("rmms1st")
        self.gridLayout.addWidget(self.rmms1st, 0, 1, 1, 1)
        self.Ytext_2 = QtWidgets.QLineEdit(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Ytext_2.sizePolicy().hasHeightForWidth())
        self.Ytext_2.setSizePolicy(sizePolicy)
        self.Ytext_2.setCursor(QtCore.Qt.ArrowCursor)
        self.Ytext_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Ytext_2.setReadOnly(True)
        self.Ytext_2.setObjectName("Ytext_2")
        self.gridLayout.addWidget(self.Ytext_2, 2, 0, 1, 1)
        self.Ytext = QtWidgets.QLineEdit(CircularCenterInput)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Ytext.sizePolicy().hasHeightForWidth())
        self.Ytext.setSizePolicy(sizePolicy)
        self.Ytext.setCursor(QtCore.Qt.ArrowCursor)
        self.Ytext.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Ytext.setReadOnly(True)
        self.Ytext.setObjectName("Ytext")
        self.gridLayout.addWidget(self.Ytext, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(CircularCenterInput)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 1)
        self.sigma_value = QtWidgets.QSpinBox(CircularCenterInput)
        self.sigma_value.setMaximum(1000)
        self.sigma_value.setProperty("value", 2)
        self.sigma_value.setObjectName("sigma_value")
        self.gridLayout.addWidget(self.sigma_value, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.restoreButton = QtWidgets.QPushButton(CircularCenterInput)
        self.restoreButton.setObjectName("restoreButton")
        self.horizontalLayout.addWidget(self.restoreButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(CircularCenterInput)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CircularCenterInput)
        QtCore.QObject.connect(self.restoreButton, QtCore.SIGNAL("clicked()"), CircularCenterInput.restore_default)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CircularCenterInput.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CircularCenterInput.reject)
        QtCore.QMetaObject.connectSlotsByName(CircularCenterInput)

    def retranslateUi(self, CircularCenterInput):
        CircularCenterInput.setWindowTitle(QtWidgets.QApplication.translate("CircularCenterInput", "Circular Center", None, -1))
        self.Xtext.setText(QtWidgets.QApplication.translate("CircularCenterInput", "rmms first ", None, -1))
        self.Ytext_2.setText(QtWidgets.QApplication.translate("CircularCenterInput", "rmms third", None, -1))
        self.Ytext.setText(QtWidgets.QApplication.translate("CircularCenterInput", "rmms second", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("CircularCenterInput", "sigma value ", None, -1))
        self.restoreButton.setText(QtWidgets.QApplication.translate("CircularCenterInput", "Restore Default", None, -1))

