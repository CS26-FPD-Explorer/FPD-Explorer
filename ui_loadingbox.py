# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadingbox.ui',
# licensing of 'loadingbox.ui' applies.
#
# Created: Wed Nov 20 19:34:09 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoadingBox(object):
    def setupUi(self, LoadingBox):
        LoadingBox.setObjectName("LoadingBox")
        LoadingBox.resize(400, 150)
        LoadingBox.setMinimumSize(QtCore.QSize(400, 144))
        LoadingBox.setMaximumSize(QtCore.QSize(400, 150))
        self.gridLayout = QtWidgets.QGridLayout(LoadingBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.realProgress = QtWidgets.QProgressBar(LoadingBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.realProgress.sizePolicy().hasHeightForWidth())
        self.realProgress.setSizePolicy(sizePolicy)
        self.realProgress.setProperty("value", 24)
        self.realProgress.setObjectName("realProgress")
        self.gridLayout_6.addWidget(self.realProgress, 1, 1, 1, 1)
        self.recipProgress = QtWidgets.QProgressBar(LoadingBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recipProgress.sizePolicy().hasHeightForWidth())
        self.recipProgress.setSizePolicy(sizePolicy)
        self.recipProgress.setProperty("value", 24)
        self.recipProgress.setObjectName("recipProgress")
        self.gridLayout_6.addWidget(self.recipProgress, 3, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(LoadingBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_6.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(LoadingBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 2, 0, 1, 1)

        self.retranslateUi(LoadingBox)
        QtCore.QMetaObject.connectSlotsByName(LoadingBox)

    def retranslateUi(self, LoadingBox):
        LoadingBox.setWindowTitle(QtWidgets.QApplication.translate("LoadingBox", "Dialog", None, -1))
        self.lineEdit_2.setText(QtWidgets.QApplication.translate("LoadingBox", "Diffraction sum images", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("LoadingBox", "Real-space sum images", None, -1))

