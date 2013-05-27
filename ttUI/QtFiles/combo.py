# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'combotest.ui'
#
# Created: Wed Feb 29 11:35:04 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.comboMode = QtGui.QComboBox(Form)
        self.comboMode.setMaxCount(2)
        self.comboMode.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboMode.setObjectName("comboMode")
        self.comboMode.addItem("Puzzle Mode")
        self.comboMode.addItem("Piece Mode")

        QtCore.QMetaObject.connectSlotsByName(Form)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

