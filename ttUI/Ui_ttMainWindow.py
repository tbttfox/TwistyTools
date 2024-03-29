# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtFiles/ttMainWindow.ui'
#
# Created: Wed Feb 29 15:24:46 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ttMainWindow(object):
    def setupUi(self, ttMainWindow):
        ttMainWindow.setObjectName("ttMainWindow")
        ttMainWindow.resize(800, 600)
        ttMainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.widCentral = QtGui.QWidget(ttMainWindow)
        self.widCentral.setObjectName("widCentral")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.widCentral)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pvViewport = ViewWindow(self.widCentral)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pvViewport.sizePolicy().hasHeightForWidth())
        self.pvViewport.setSizePolicy(sizePolicy)
        self.pvViewport.setObjectName("pvViewport")
        self.verticalLayout_7.addWidget(self.pvViewport)
        ttMainWindow.setCentralWidget(self.widCentral)
        self.hierarchyDockWidget = QtGui.QDockWidget(ttMainWindow)
        self.hierarchyDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.hierarchyDockWidget.setObjectName("hierarchyDockWidget")
        self.widTreeDesign = QtGui.QWidget()
        self.widTreeDesign.setObjectName("widTreeDesign")
        self.verticalLayout = QtGui.QVBoxLayout(self.widTreeDesign)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeDesign = PuzzleTreeView(self.widTreeDesign)
        self.treeDesign.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeDesign.sizePolicy().hasHeightForWidth())
        self.treeDesign.setSizePolicy(sizePolicy)
        self.treeDesign.setMinimumSize(QtCore.QSize(200, 0))
        self.treeDesign.setFrameShape(QtGui.QFrame.WinPanel)
        self.treeDesign.setFrameShadow(QtGui.QFrame.Sunken)
        self.treeDesign.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.treeDesign.setAlternatingRowColors(True)
        self.treeDesign.setRootIsDecorated(False)
        self.treeDesign.setAllColumnsShowFocus(True)
        self.treeDesign.setObjectName("treeDesign")
        self.treeDesign.header().setDefaultSectionSize(200)
        self.treeDesign.header().setMinimumSectionSize(50)
        self.verticalLayout.addWidget(self.treeDesign)
        self.hierarchyDockWidget.setWidget(self.widTreeDesign)
        ttMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.hierarchyDockWidget)
        self.pieceDockWidget = QtGui.QDockWidget(ttMainWindow)
        self.pieceDockWidget.setMinimumSize(QtCore.QSize(112, 132))
        self.pieceDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.pieceDockWidget.setObjectName("pieceDockWidget")
        self.widPieceEdit = QtGui.QWidget()
        self.widPieceEdit.setObjectName("widPieceEdit")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widPieceEdit)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tblPieceEdit = PieceEditGrid(self.widPieceEdit)
        self.tblPieceEdit.setObjectName("tblPieceEdit")
        self.verticalLayout_3.addWidget(self.tblPieceEdit)
        self.pieceDockWidget.setWidget(self.widPieceEdit)
        ttMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.pieceDockWidget)
        self.toolBar = QtGui.QToolBar(ttMainWindow)
        self.toolBar.setObjectName("toolBar")
        ttMainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionNew = QtGui.QAction(ttMainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtGui.QAction(ttMainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_AS = QtGui.QAction(ttMainWindow)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionOpen = QtGui.QAction(ttMainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtGui.QAction(ttMainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCut = QtGui.QAction(ttMainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtGui.QAction(ttMainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtGui.QAction(ttMainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionPreferences = QtGui.QAction(ttMainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionNew_Layer = QtGui.QAction(ttMainWindow)
        self.actionNew_Layer.setObjectName("actionNew_Layer")
        self.actionSymmetry = QtGui.QAction(ttMainWindow)
        self.actionSymmetry.setObjectName("actionSymmetry")
        self.actionNew_Vector = QtGui.QAction(ttMainWindow)
        self.actionNew_Vector.setObjectName("actionNew_Vector")
        self.actionTwistyTools_Help = QtGui.QAction(ttMainWindow)
        self.actionTwistyTools_Help.setObjectName("actionTwistyTools_Help")
        self.actionAbout = QtGui.QAction(ttMainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(ttMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ttMainWindow)

    def retranslateUi(self, ttMainWindow):
        ttMainWindow.setWindowTitle(QtGui.QApplication.translate("ttMainWindow", "Twisty Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.hierarchyDockWidget.setWindowTitle(QtGui.QApplication.translate("ttMainWindow", "Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.pieceDockWidget.setWindowTitle(QtGui.QApplication.translate("ttMainWindow", "Piece Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("ttMainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("ttMainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("ttMainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_AS.setText(QtGui.QApplication.translate("ttMainWindow", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("ttMainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("ttMainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("ttMainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("ttMainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("ttMainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("ttMainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Layer.setText(QtGui.QApplication.translate("ttMainWindow", "New Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSymmetry.setText(QtGui.QApplication.translate("ttMainWindow", "Symmetry", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Vector.setText(QtGui.QApplication.translate("ttMainWindow", "New Vector", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTwistyTools_Help.setText(QtGui.QApplication.translate("ttMainWindow", "TwistyTools Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("ttMainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

from puzzletreeview import PuzzleTreeView
from viewwindow import ViewWindow
from pieceeditgrid import PieceEditGrid
