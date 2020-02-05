from PySide2 import QtWidgets

class UI_Generator(QtWidgets.QDialog):
    """
    Initialize the required widget needed by DPC explorer tab

    Parameters
    ----------
    ApplicationWindow : QApplication
        The parent in which the tab should be rendered
    mainwindow : QMainWindow 
        The main window in which the dock widget should get created
    fnct : function
        The function object for which we want to create the input box

    """

    def __init__(self, ApplicationWindow, mainwindow, fnct):
        super(UI_Generator, self).__init__()
        self.application_window = ApplicationWindow
        self.main_window = mainwindow
        self.param = self.get_param_docstring(fnct)

    def get_param_docstring(self, fnct):
        doc = fnct.__doc__
        result = []
        tmp = []
        param = doc.split('Parameters')[1].replace(',','').replace('-','').split("Return")[0].split('\n')
        counter = 0
        for idx, el in enumerate(param):
            if not el.isspace() and el:
                if el.find(':') != -1:
                    if tmp != []:
                        result.append(tmp)
                        tmp = []
                    counter = 0
                    tmp.extend(el.lstrip().split(':'))
                if counter > 0:
                    tmp.append(param[idx].lstrip())
                    if len(tmp) > 2 :
                        tmp[2] = " ".join(tmp[2:])
                        del tmp[3:]
                counter += 1
        result.append(tmp)    
        return result


