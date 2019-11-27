from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog#, QDialog
from PySide2 import QtWidgets#, QtCore, QtGui
from PySide2.QtCore import Slot
from ui_homescreen import Ui_MainWindow
import sys
# import os

# progname = os.path.basename(sys.argv[0])

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.last_path = ""


    @Slot()
    def function_mib(self):
        print("print from function_mib")
        fname, fother = QFileDialog.getOpenFileName(
        self, 'Open file', self.last_path, "MERLIN binary files (*.mib)")
        print(fname, fother)
        if fname: 
            if fname[-3:] == "mib": # empty string means user canceled
                self.last_path = fname
                self.mib_path = fname
                self.ui.mib_line.clear()
                self.ui.mib_line.insert(fname)
                return True
        return False


    @Slot()
    def LoadFiles(self):
        x_value = None
        y_value = None
        #Cherk if Mib exist
        try:
            mib = self.mib_path
        except AttributeError:
            response = QtWidgets.QMessageBox.warning(
                self, "Warning", "<strong>We noticed you don't have a Merlin Binary File</strong> <br> Do you want to select one ?",
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                valid = self.function_mib()  # load a .mib file and use it
                if not valid: #user canceled
                    return 
            else:
                return

qApp = QtWidgets.QApplication()

aw = ApplicationWindow()
# aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
