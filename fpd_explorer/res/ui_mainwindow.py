# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fpd_explorer\res\mainwindow.ui',
# licensing of '.\fpd_explorer\res\mainwindow.ui' applies.
#
# Created: Fri Jan 24 21:15:25 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 640)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.MIB = QtWidgets.QLineEdit(self.centralWidget)
        self.MIB.setInputMask("")
        self.MIB.setText("")
        self.MIB.setReadOnly(True)
        self.MIB.setClearButtonEnabled(True)
        self.MIB.setObjectName("MIB")
        self.gridLayout_5.addWidget(self.MIB, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_5.addWidget(self.pushButton, 0, 3, 1, 1)
        self.DM3 = QtWidgets.QLineEdit(self.centralWidget)
        self.DM3.setInputMask("")
        self.DM3.setText("")
        self.DM3.setReadOnly(True)
        self.DM3.setClearButtonEnabled(True)
        self.DM3.setObjectName("DM3")
        self.gridLayout_5.addWidget(self.DM3, 0, 1, 1, 1)
        self.darkModeButton = QtWidgets.QCheckBox(self.centralWidget)
        self.darkModeButton.setObjectName("darkModeButton")
        self.gridLayout_5.addWidget(self.darkModeButton, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1088, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu_file = QtWidgets.QMenu(self.menuBar)
        self.menu_file.setObjectName("menu_file")
        self.menu_Open = QtWidgets.QMenu(self.menu_file)
        self.menu_Open.setObjectName("menu_Open")
        self.menuFunctions = QtWidgets.QMenu(self.menu_file)
        self.menuFunctions.setObjectName("menuFunctions")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
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
        self.navCanvas = MyMplCanvas(self.dockWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navCanvas.sizePolicy().hasHeightForWidth())
        self.navCanvas.setSizePolicy(sizePolicy)
        self.navCanvas.setObjectName("navCanvas")
        self.gridLayout.addWidget(self.navCanvas, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.navX = QtWidgets.QSpinBox(self.dockWidgetContents_8)
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
        self.navY = QtWidgets.QSpinBox(self.dockWidgetContents_8)
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
        self.lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.dockWidgetContents_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_6.addWidget(self.lineEdit_2, 0, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 0, 0, 1, 1)
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
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.dockWidgetContents_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_7.addWidget(self.lineEdit_4, 0, 0, 1, 1)
        self.colorMap = QtWidgets.QComboBox(self.dockWidgetContents_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorMap.sizePolicy().hasHeightForWidth())
        self.colorMap.setSizePolicy(sizePolicy)
        self.colorMap.setCurrentText("")
        self.colorMap.setObjectName("colorMap")
        self.gridLayout_7.addWidget(self.colorMap, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.diffCanvas = MyMplCanvas(self.dockWidgetContents_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffCanvas.sizePolicy().hasHeightForWidth())
        self.diffCanvas.setSizePolicy(sizePolicy)
        self.diffCanvas.setObjectName("diffCanvas")
        self.gridLayout_2.addWidget(self.diffCanvas, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)
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
        self.action_Find_Circular_Center = QtWidgets.QAction(MainWindow)
        self.action_Find_Circular_Center.setObjectName("action_Find_Circular_Center")
        self.action_Remove_Aperture = QtWidgets.QAction(MainWindow)
        self.action_Remove_Aperture.setObjectName("action_Remove_Aperture")
        self.action_Center_of_Mass = QtWidgets.QAction(MainWindow)
        self.action_Center_of_Mass.setObjectName("action_Center_of_Mass")
        self.menu_Open.addAction(self.action_dm3)
        self.menu_Open.addAction(self.action_mib)
        self.menu_Open.addAction(self.action_hdf5)
        self.menuFunctions.addAction(self.action_Find_Circular_Center)
        self.menuFunctions.addAction(self.action_Remove_Aperture)
        self.menuFunctions.addAction(self.action_Center_of_Mass)
        self.menu_file.addAction(self.menu_Open.menuAction())
        self.menu_file.addAction(self.menuFunctions.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainWindow.load_files)
        QtCore.QObject.connect(self.navY, QtCore.SIGNAL("valueChanged(int)"), MainWindow.update_rect)
        QtCore.QObject.connect(self.navX, QtCore.SIGNAL("valueChanged(int)"), MainWindow.update_rect)
        QtCore.QObject.connect(self.colorMap, QtCore.SIGNAL("currentIndexChanged(QString)"), MainWindow.update_color_map)
        QtCore.QObject.connect(self.darkModeButton, QtCore.SIGNAL("clicked()"), MainWindow.change_color_mode)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.DM3, self.MIB)
        MainWindow.setTabOrder(self.MIB, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.navX)
        MainWindow.setTabOrder(self.navX, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.navY)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "FpdExplorer", None, -1))
        self.MIB.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Merlin Binary Path", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))
        self.DM3.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "DM3 Path", None, -1))
        self.darkModeButton.setText(QtWidgets.QApplication.translate("MainWindow", "Dark Mode", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "&File", None, -1))
        self.menu_Open.setTitle(QtWidgets.QApplication.translate("MainWindow", "&Open", None, -1))
        self.menuFunctions.setTitle(QtWidgets.QApplication.translate("MainWindow", "Functions ", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.navigationWidget.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Navigation", None, -1))
        self.lineEdit.setText(QtWidgets.QApplication.translate("MainWindow", "X size", None, -1))
        self.lineEdit_2.setText(QtWidgets.QApplication.translate("MainWindow", "Y size", None, -1))
        self.diffractionWidget.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Diffraction", None, -1))
        self.lineEdit_4.setText(QtWidgets.QApplication.translate("MainWindow", "Color Map", None, -1))
        self.action_dm3.setText(QtWidgets.QApplication.translate("MainWindow", "&.dm3", None, -1))
        self.action_mib.setText(QtWidgets.QApplication.translate("MainWindow", "&.mib", None, -1))
        self.action_hdf5.setText(QtWidgets.QApplication.translate("MainWindow", "&.hdf5", None, -1))
        self.action_about.setText(QtWidgets.QApplication.translate("MainWindow", "&About", None, -1))
        self.action_Find_Circular_Center.setText(QtWidgets.QApplication.translate("MainWindow", "Find Circular Center", None, -1))
        self.action_Remove_Aperture.setText(QtWidgets.QApplication.translate("MainWindow", "Remove Aperture", None, -1))
        self.action_Center_of_Mass.setText(QtWidgets.QApplication.translate("MainWindow", "Center of Mass", None, -1))

from custom_widgets import MyMplCanvas
