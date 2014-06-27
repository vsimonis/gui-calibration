# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confSystem.ui'
#
# Created: Thu Jun 26 20:29:19 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1772, 1155)
        MainWindow.setMinimumSize(QtCore.QSize(1400, 1100))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.videoFrame = QtWidgets.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(20, 10, 1280, 960))
        self.videoFrame.setText("")
        self.videoFrame.setObjectName("videoFrame")
        
        self.changeWidth = QtWidgets.QTextEdit(self.centralwidget)
        self.changeWidth.setGeometry(QtCore.QRect(1340, 90, 351, 51))
        self.changeWidth.setObjectName("changeWidth")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1340, 24, 361, 51))
        self.label.setObjectName("label")
        
        self.buttonCenter = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCenter.setGeometry(QtCore.QRect(1340, 190, 351, 57))
        self.buttonCenter.setObjectName("buttonCenter")
        
        self.buttonUndo = QtWidgets.QPushButton(self.centralwidget)
        self.buttonUndo.setGeometry(QtCore.QRect(1340, 280, 351, 57))
        self.buttonUndo.setObjectName("buttonUndo")
        
        self.buttonAccept = QtWidgets.QPushButton(self.centralwidget)
        self.buttonAccept.setGeometry(QtCore.QRect(1340, 370, 351, 57))
        self.buttonAccept.setToolTip("")
        self.buttonAccept.setObjectName("buttonAccept")
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1310, 0, 411, 571))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1772, 56))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.changeWidth.textChanged.connect(self.statusbar.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Frame width (in mm)"))
        self.buttonCenter.setText(_translate("MainWindow", "Center"))
        self.buttonUndo.setText(_translate("MainWindow", "Undo"))
        self.buttonAccept.setText(_translate("MainWindow", "Accept"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


