# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Sun Nov 10 22:02:21 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 636)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_5.addWidget(self.pushButton, 0, 2, 1, 1)
        self.DM3 = QtWidgets.QLineEdit(self.centralWidget)
        self.DM3.setInputMask("")
        self.DM3.setText("")
        self.DM3.setReadOnly(True)
        self.DM3.setClearButtonEnabled(True)
        self.DM3.setObjectName("DM3")
        self.gridLayout_5.addWidget(self.DM3, 0, 0, 1, 1)
        self.MIB = QtWidgets.QLineEdit(self.centralWidget)
        self.MIB.setInputMask("")
        self.MIB.setText("")
        self.MIB.setReadOnly(True)
        self.MIB.setClearButtonEnabled(True)
        self.MIB.setObjectName("MIB")
        self.gridLayout_5.addWidget(self.MIB, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1088, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu_file = QtWidgets.QMenu(self.menuBar)
        self.menu_file.setObjectName("menu_file")
        self.menu_Open = QtWidgets.QMenu(self.menu_file)
        self.menu_Open.setObjectName("menu_Open")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.navigationWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.navigationWidget.sizePolicy().hasHeightForWidth())
        self.navigationWidget.setSizePolicy(sizePolicy)
        self.navigationWidget.setMinimumSize(QtCore.QSize(541, 541))
        self.navigationWidget.setFloating(False)
        self.navigationWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.navigationWidget.setObjectName("navigationWidget")
        self.dockWidgetContents_8 = QtWidgets.QWidget()
        self.dockWidgetContents_8.setObjectName("dockWidgetContents_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.widget_3 = MyMplCanvas(self.dockWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout.addWidget(self.widget_3, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.navigationWidget.setWidget(self.dockWidgetContents_8)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.navigationWidget)
        self.diffractionWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.diffractionWidget.sizePolicy().hasHeightForWidth())
        self.diffractionWidget.setSizePolicy(sizePolicy)
        self.diffractionWidget.setMinimumSize(QtCore.QSize(541, 541))
        self.diffractionWidget.setFloating(False)
        self.diffractionWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.diffractionWidget.setObjectName("diffractionWidget")
        self.dockWidgetContents_9 = QtWidgets.QWidget()
        self.dockWidgetContents_9.setObjectName("dockWidgetContents_9")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_4 = MyMplCanvas(self.dockWidgetContents_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_2.addWidget(self.widget_4, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.diffractionWidget.setWidget(self.dockWidgetContents_9)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.diffractionWidget)
        self.action_dm3 = QtWidgets.QAction(MainWindow)
        self.action_dm3.setObjectName("action_dm3")
        self.action_mib = QtWidgets.QAction(MainWindow)
        self.action_mib.setObjectName("action_mib")
        self.action_hdf5 = QtWidgets.QAction(MainWindow)
        self.action_hdf5.setObjectName("action_hdf5")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menu_Open.addAction(self.action_dm3)
        self.menu_Open.addAction(self.action_mib)
        self.menu_Open.addAction(self.action_hdf5)
        self.menu_file.addAction(self.menu_Open.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainWindow.LoadFiles)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "FpdExplorer", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.DM3.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "DM3 Path", None, -1))
        self.MIB.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Merlin Binary Path", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "&File", None, -1))
        self.menu_Open.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Open", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1))
        self.navigationWidget.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Navigation", None, -1))
        self.diffractionWidget.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Diffraction", None, -1))
        self.action_dm3.setText(QtWidgets.QApplication.translate("MainWindow", "&.dm3", None, -1))
        self.action_mib.setText(QtWidgets.QApplication.translate("MainWindow", "&.mib", None, -1))
        self.action_hdf5.setText(QtWidgets.QApplication.translate("MainWindow", "&.hdf5", None, -1))
        self.action_about.setText(QtWidgets.QApplication.translate("MainWindow", "&About", None, -1))

from custom_widgets import MyMplCanvas
