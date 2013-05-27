from PyQt4 import QtGui 
def warningMessage(message, title = "Warning"):
    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, title, message, QtGui.QMessageBox.NoButton)
    msgBox.addButton("&OK", QtGui.QMessageBox.AcceptRole)
    msgBox.exec_()


