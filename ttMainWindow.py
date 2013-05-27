#!/usr/bin/python

##############################################################################
#    TwistyTools: A program for designing arbitrary Rubik's Cube like puzzles
#    Copyright (C) 2013 Tyler J. Fox
##############################################################################

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from ttUI.Ui_ttMainWindow import Ui_ttMainWindow
from ttUI.puzzletreeview import TreeModel


from ttLib.puzzleinterface import PuzzleInterface
from ttLib.ttMkPuzzle import defaultPuzzle


class TwistyTools(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(TwistyTools, self).__init__(parent)
        self.graphSliders = []
        self.ui = Ui_ttMainWindow()
        self.ui.setupUi(self)
        self.mkActions()
        self.setupToolbar()
        self.puzzleInit()
        self.viewportSetup()
        self.treeSetup()
        self.gridSetup()
        #self.ui.pieceDockWidget.hide()

    def puzzleInit(self):
        self.puzzle = defaultPuzzle()
        self.puzzleInterface = PuzzleInterface(self.puzzle)

    def viewportSetup(self):
        self.ui.pvViewport.registerPuzzle(self.puzzleInterface)

    def treeSetup(self):
        self.treeModel = TreeModel(self.puzzleInterface)
        self.ui.treeDesign.setModel(self.treeModel)
        self.ui.treeDesign.header().resizeSection(0,150)
        self.ui.treeDesign.header().resizeSection(1,1)

    def gridSetup(self):
        self.ui.tblPieceEdit.registerPuzzle(self.puzzleInterface)


    def mkActions(self):
        ui = self.ui
        ui.actionNew = QtGui.QAction(
                QtGui.QIcon.fromTheme("document-new"), "&New",
                self, shortcut="Ctrl+N", statusTip="Create a New Puzzle",
                triggered=self.newPuzzle)

        ui.actionSave = QtGui.QAction(
                QtGui.QIcon.fromTheme("document-save"), "&Save",
                self, shortcut="Ctrl+S", statusTip="Save the current file",
                triggered=self.savePuzzle)

        ui.actionSave_As = QtGui.QAction(
                QtGui.QIcon.fromTheme("document-save-as"), "Save As",
                self, statusTip="Save As New File",
                triggered=self.saveAsPuzzle)

        ui.actionOpen = QtGui.QAction(
                QtGui.QIcon.fromTheme("document-open"), "&Open",
                self, shortcut="Ctrl+O", statusTip="Open a File",
                triggered=self.openPuzzle)

        ui.actionQuit = QtGui.QAction(
                QtGui.QIcon.fromTheme("application-exit"), "&Quit",
                self, shortcut="Ctrl+Q", statusTip="Quit TwistyTools",
                triggered=self.quitProgram)

        ui.actionAbout = QtGui.QAction(
                QtGui.QIcon.fromTheme("help-about"), "&About",
                self, shortcut="Ctrl+A", statusTip="About TwistyTools",
                triggered=self.aboutProgram)

        ui.actionBreak = QtGui.QAction(
                QtGui.QIcon.fromTheme("process-stop"), "&Break",
                self, shortcut="Ctrl+B", statusTip="Debug Break",
                triggered=self.debugBreak)

    def setupToolbar(self):
        ui = self.ui
        ui.toolBar.addAction(ui.actionNew)
        ui.toolBar.addAction(ui.actionOpen)
        ui.toolBar.addAction(ui.actionSave)
        ui.toolBar.addAction(ui.actionSave_As)
        ui.toolBar.addAction(ui.actionBreak)

        ui.comboMode = QtGui.QComboBox()
        ui.comboMode.setMaxCount(2)
        ui.comboMode.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        ui.comboMode.setObjectName("comboMode")
        ui.comboMode.addItem("Puzzle Mode")
        ui.comboMode.addItem("Piece Mode")
        ui.toolBar.addWidget(ui.comboMode)
        ui.comboMode.currentIndexChanged.connect(self.changeMode)

    def newPuzzle(self):
        print "New Puzzle"

    def savePuzzle(self):
        print "Save Puzzle"

    def saveAsPuzzle(self):
        print "SaveAs Puzzle"

    def openPuzzle(self):
        print "Open New Puzzle"

    def quitProgram(self):
        print "Quit"

    def aboutProgram(self):
        print "About"

    def debugBreak(self):
        import myDB
        myDB.setTrace()

    def changeMode(self):
        index = self.ui.comboMode.currentIndex()
        if index == 0: # puzzle mode
            #already done
            self.ui.pieceDockWidget.hide()
            self.ui.hierarchyDockWidget.show()
            self.puzzleInterface.drawMode = PuzzleInterface.puzzleDrawMode
        else: # piece mode
            #add buttons for clickthroughs
            #probably need some kind of fog/transparency
            self.ui.hierarchyDockWidget.hide()
            self.ui.pieceDockWidget.show()
            self.puzzleInterface.drawMode = PuzzleInterface.pieceDrawMode


if __name__ == "__main__":
    sys.setrecursionlimit(100)
    app = QtGui.QApplication(sys.argv)
    ttApp = TwistyTools()
    ttApp.show()
    sys.exit(app.exec_())


