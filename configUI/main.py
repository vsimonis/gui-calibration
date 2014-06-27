from PyQt5 import QtGui, QtCore, QtWidgets 
import configUI
import managers

class Gui(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cap = man