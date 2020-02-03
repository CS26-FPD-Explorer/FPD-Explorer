# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fpd_explorer\res\homescreen.ui',
# licensing of '.\fpd_explorer\res\homescreen.ui' applies.
#
# Created: Mon Feb  3 22:25:26 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(1050, 625))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.home_tab = QtWidgets.QWidget()
        self.home_tab.setObjectName("home_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.home_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.workflow_groupBox = QtWidgets.QGroupBox(self.home_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workflow_groupBox.sizePolicy().hasHeightForWidth())
        self.workflow_groupBox.setSizePolicy(sizePolicy)
        self.workflow_groupBox.setMinimumSize(QtCore.QSize(500, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.workflow_groupBox.setFont(font)
        self.workflow_groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.workflow_groupBox.setAutoFillBackground(False)
        self.workflow_groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.workflow_groupBox.setFlat(False)
        self.workflow_groupBox.setObjectName("workflow_groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.workflow_groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout.addWidget(self.workflow_groupBox, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.functions_groupBox = QtWidgets.QGroupBox(self.home_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functions_groupBox.sizePolicy().hasHeightForWidth())
        self.functions_groupBox.setSizePolicy(sizePolicy)
        self.functions_groupBox.setMinimumSize(QtCore.QSize(500, 0))
        self.functions_groupBox.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.functions_groupBox.setFont(font)
        self.functions_groupBox.setObjectName("functions_groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.functions_groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_43 = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.pushButton_43.setFont(font)
        self.pushButton_43.setCheckable(False)
        self.pushButton_43.setFlat(False)
        self.pushButton_43.setObjectName("pushButton_43")
        self.gridLayout_3.addWidget(self.pushButton_43, 1, 1, 1, 1)
        self.centre_of_mass_button = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.centre_of_mass_button.setFont(font)
        self.centre_of_mass_button.setCheckable(False)
        self.centre_of_mass_button.setFlat(False)
        self.centre_of_mass_button.setObjectName("centre_of_mass_button")
        self.gridLayout_3.addWidget(self.centre_of_mass_button, 3, 0, 1, 1)
        self.pushButton_42 = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.pushButton_42.setFont(font)
        self.pushButton_42.setCheckable(False)
        self.pushButton_42.setFlat(False)
        self.pushButton_42.setObjectName("pushButton_42")
        self.gridLayout_3.addWidget(self.pushButton_42, 2, 1, 1, 1)
        self.dbrowser_button = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.dbrowser_button.setFont(font)
        self.dbrowser_button.setCheckable(False)
        self.dbrowser_button.setFlat(False)
        self.dbrowser_button.setObjectName("dbrowser_button")
        self.gridLayout_3.addWidget(self.dbrowser_button, 0, 0, 1, 1)
        self.rm_aperture_button = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.rm_aperture_button.setFont(font)
        self.rm_aperture_button.setCheckable(False)
        self.rm_aperture_button.setFlat(False)
        self.rm_aperture_button.setObjectName("rm_aperture_button")
        self.gridLayout_3.addWidget(self.rm_aperture_button, 2, 0, 1, 1)
        self.find_circ_c_button = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.find_circ_c_button.setFont(font)
        self.find_circ_c_button.setCheckable(False)
        self.find_circ_c_button.setFlat(False)
        self.find_circ_c_button.setObjectName("find_circ_c_button")
        self.gridLayout_3.addWidget(self.find_circ_c_button, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 1, 1, 1)
        self.pushButton_41 = QtWidgets.QPushButton(self.functions_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.pushButton_41.setFont(font)
        self.pushButton_41.setCheckable(False)
        self.pushButton_41.setFlat(False)
        self.pushButton_41.setObjectName("pushButton_41")
        self.gridLayout_3.addWidget(self.pushButton_41, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.functions_groupBox, 1, 3, 1, 1)
        self.file_groupBox = QtWidgets.QGroupBox(self.home_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_groupBox.sizePolicy().hasHeightForWidth())
        self.file_groupBox.setSizePolicy(sizePolicy)
        self.file_groupBox.setMinimumSize(QtCore.QSize(500, 0))
        self.file_groupBox.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.file_groupBox.setFont(font)
        self.file_groupBox.setObjectName("file_groupBox")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.file_groupBox)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mib_button = QtWidgets.QPushButton(self.file_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.mib_button.setFont(font)
        self.mib_button.setCheckable(False)
        self.mib_button.setFlat(False)
        self.mib_button.setObjectName("mib_button")
        self.horizontalLayout.addWidget(self.mib_button)
        self.dm3_button = QtWidgets.QPushButton(self.file_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.dm3_button.setFont(font)
        self.dm3_button.setCheckable(False)
        self.dm3_button.setFlat(False)
        self.dm3_button.setObjectName("dm3_button")
        self.horizontalLayout.addWidget(self.dm3_button)
        self.hdf5_button = QtWidgets.QPushButton(self.file_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.hdf5_button.setFont(font)
        self.hdf5_button.setCheckable(False)
        self.hdf5_button.setFlat(False)
        self.hdf5_button.setObjectName("hdf5_button")
        self.horizontalLayout.addWidget(self.hdf5_button)
        self.verticalLayout_11.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mib_line = QtWidgets.QLineEdit(self.file_groupBox)
        self.mib_line.setInputMask("")
        self.mib_line.setText("")
        self.mib_line.setReadOnly(True)
        self.mib_line.setClearButtonEnabled(False)
        self.mib_line.setObjectName("mib_line")
        self.verticalLayout_3.addWidget(self.mib_line)
        self.dm3_line = QtWidgets.QLineEdit(self.file_groupBox)
        self.dm3_line.setInputMask("")
        self.dm3_line.setText("")
        self.dm3_line.setReadOnly(True)
        self.dm3_line.setClearButtonEnabled(False)
        self.dm3_line.setObjectName("dm3_line")
        self.verticalLayout_3.addWidget(self.dm3_line)
        self.hdf5_line = QtWidgets.QLineEdit(self.file_groupBox)
        self.hdf5_line.setAutoFillBackground(False)
        self.hdf5_line.setInputMask("")
        self.hdf5_line.setText("")
        self.hdf5_line.setReadOnly(True)
        self.hdf5_line.setClearButtonEnabled(False)
        self.hdf5_line.setObjectName("hdf5_line")
        self.verticalLayout_3.addWidget(self.hdf5_line)
        self.verticalLayout_11.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.load_button = QtWidgets.QPushButton(self.file_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.load_button.setFont(font)
        self.load_button.setCheckable(False)
        self.load_button.setFlat(False)
        self.load_button.setObjectName("load_button")
        self.horizontalLayout_2.addWidget(self.load_button)
        self.clear_button = QtWidgets.QPushButton(self.file_groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.clear_button.setFont(font)
        self.clear_button.setCheckable(False)
        self.clear_button.setFlat(False)
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout_2.addWidget(self.clear_button)
        self.verticalLayout_11.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.file_groupBox, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem3, 2, 3, 1, 1)
        self.resource_groupBox = QtWidgets.QGroupBox(self.home_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resource_groupBox.sizePolicy().hasHeightForWidth())
        self.resource_groupBox.setSizePolicy(sizePolicy)
        self.resource_groupBox.setMinimumSize(QtCore.QSize(500, 300))
        self.resource_groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.resource_groupBox.setFont(font)
        self.resource_groupBox.setObjectName("resource_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.resource_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.resMonitor = CpuFreqGraph(self.resource_groupBox)
        self.resMonitor.setObjectName("resMonitor")
        self.gridLayout_4.addWidget(self.resMonitor, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.resource_groupBox, 3, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 4, 1, 1, 1)
        self.tabWidget.addTab(self.home_tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.dark_mode_button = QtWidgets.QCheckBox(self.centralwidget)
        self.dark_mode_button.setObjectName("dark_mode_button")
        self.gridLayout_2.addWidget(self.dark_mode_button, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_dm3 = QtWidgets.QAction(MainWindow)
        self.action_dm3.setObjectName("action_dm3")
        self.action_mib = QtWidgets.QAction(MainWindow)
        self.action_mib.setObjectName("action_mib")
        self.action_hdf5 = QtWidgets.QAction(MainWindow)
        self.action_hdf5.setObjectName("action_hdf5")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menuOpen.addAction(self.action_mib)
        self.menuOpen.addAction(self.action_dm3)
        self.menuOpen.addAction(self.action_hdf5)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.mib_button, QtCore.SIGNAL("clicked()"), MainWindow.function_mib)
        QtCore.QObject.connect(self.dbrowser_button, QtCore.SIGNAL("clicked()"), MainWindow.start_dbrowser)
        QtCore.QObject.connect(self.find_circ_c_button, QtCore.SIGNAL("clicked()"), MainWindow.find_circular_centre)
        QtCore.QObject.connect(self.load_button, QtCore.SIGNAL("clicked()"), MainWindow.load_files)
        QtCore.QObject.connect(self.dm3_button, QtCore.SIGNAL("clicked()"), MainWindow.function_dm3)
        QtCore.QObject.connect(self.clear_button, QtCore.SIGNAL("clicked()"), MainWindow.clear_files)
        QtCore.QObject.connect(self.dark_mode_button, QtCore.SIGNAL("clicked()"), MainWindow.change_color_mode)
        QtCore.QObject.connect(self.rm_aperture_button, QtCore.SIGNAL("clicked()"), MainWindow.remove_aperture)
        QtCore.QObject.connect(self.centre_of_mass_button, QtCore.SIGNAL("clicked()"), MainWindow.centre_of_mass)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "fpd gui", None, -1))
        self.workflow_groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Workflow help", None, -1))
        self.functions_groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Functions", None, -1))
        self.pushButton_43.setText(QtWidgets.QApplication.translate("MainWindow", "Dummy", None, -1))
        self.centre_of_mass_button.setText(QtWidgets.QApplication.translate("MainWindow", "centre_of_mass", None, -1))
        self.pushButton_42.setText(QtWidgets.QApplication.translate("MainWindow", "Dummy", None, -1))
        self.dbrowser_button.setText(QtWidgets.QApplication.translate("MainWindow", "DataBrowser", None, -1))
        self.rm_aperture_button.setText(QtWidgets.QApplication.translate("MainWindow", "synthetic_aperture", None, -1))
        self.find_circ_c_button.setText(QtWidgets.QApplication.translate("MainWindow", "find_circ_centre", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Dummy", None, -1))
        self.pushButton_41.setText(QtWidgets.QApplication.translate("MainWindow", "Dummy", None, -1))
        self.file_groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "File opening", None, -1))
        self.mib_button.setText(QtWidgets.QApplication.translate("MainWindow", ".mib", None, -1))
        self.dm3_button.setText(QtWidgets.QApplication.translate("MainWindow", ".dm3", None, -1))
        self.hdf5_button.setText(QtWidgets.QApplication.translate("MainWindow", ".hdf5", None, -1))
        self.mib_line.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", ".mib filename", None, -1))
        self.dm3_line.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", ".dm3 filename", None, -1))
        self.hdf5_line.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", ".hdf5 filename", None, -1))
        self.load_button.setText(QtWidgets.QApplication.translate("MainWindow", "Load", None, -1))
        self.clear_button.setText(QtWidgets.QApplication.translate("MainWindow", "Clear", None, -1))
        self.resource_groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Resource monitor", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home_tab), QtWidgets.QApplication.translate("MainWindow", "Home", None, -1))
        self.dark_mode_button.setText(QtWidgets.QApplication.translate("MainWindow", "Dark Mode", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuOpen.setTitle(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.action_dm3.setText(QtWidgets.QApplication.translate("MainWindow", ".dm3", None, -1))
        self.action_mib.setText(QtWidgets.QApplication.translate("MainWindow", ".mib", None, -1))
        self.action_hdf5.setText(QtWidgets.QApplication.translate("MainWindow", ".hdf5", None, -1))
        self.action_about.setText(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))

from fpd_explorer.resource_monitor import CpuFreqGraph
