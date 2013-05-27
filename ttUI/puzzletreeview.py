#!/usr/bin/python
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from ttLib.ttSymmetry import Symmetry
from ttLib.ttValue import Value
from ttLib.ttBase import TTBase
from ttLib.puzzleinterface import PuzzleInterface

from warnings import warningMessage


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, puzzle, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootData = Value("Value","Item")
        self.rootItem = TreeItem(self.rootData)
        self.puzzleInterface = puzzle #This will be a puzzleInterface
        self.setupPuzzleData(self.puzzleInterface.puzzle,self.rootItem)

    def setupPuzzleData(self,item, par):
        par.insertChild(par.childCount(), item)
        nextPar = par.child(par.childCount()-1)
        for puzPar in self.puzzleInterface.itemChildren(item):
            self.setupPuzzleData(puzPar,nextPar)

    def columnCount(self, parent):
        return 2

    def flags(self, index):
        if not index.isValid():
            return 0
        #I don't remember why these 3 lines are here ... take them out at some point in time to 
        #figure out where the circles are coming from
        thingType = index.internalPointer().itemData.enum
        if thingType == TTBase.enumType.Circle:
            return Qt.ItemIsSelectable 
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertRows(self, position, rows, parent=QtCore.QModelIndex(),value=Value("None","None")):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows, value)
        self.endInsertRows()

        return success

    def newShell(self, position, parent, shell):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position,position)

        parentItem.insertChild(position, shell)
        nextPar = parentItem.child(position)
        if shell.children:
            for puzPar in shell.children:
                self.setupPuzzleData(puzPar,nextPar)

        self.endInsertRows()

    def newFactory(self, parent, factory):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, parentItem.childCount(),parentItem.childCount())
        
        parentItem.insertChild(parentItem.childCount(), factory)
        nextPar = parentItem.child(parentItem.childCount()-1)
        if factory.children:
            for puzPar in factory.children:
                self.setupPuzzleData(puzPar,nextPar)

        self.endInsertRows()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        return parentItem.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            item = self.getItem(index)
            return item.data(index.column())
        elif role == Qt.CheckStateRole:
            if index.column() == 0:
                if index.internalPointer().itemData.enum in (TTBase.enumType.Shell, TTBase.enumType.CircleFactory, TTBase.enumType.Sphere):
                    item = index.internalPointer()
                    return item.isChecked()
        elif role == Qt.DecorationRole:
            #if color is None,  inherit the color from the child
            #otherwise return the color
            if index.column() == 0:
                if index.internalPointer().itemData.enum in (TTBase.enumType.Shell, TTBase.enumType.Graph, TTBase.enumType.Sphere, TTBase.enumType.Puzzle):
                    if index.internalPointer().itemData.inheritsColor():
                        return QtGui.QIcon.fromTheme("go-up")
                    else:
                        c = [int(i * 255) for i in index.internalPointer().itemData.color]
                        return QtGui.QColor(*c[:3])
        elif role == Qt.SizeHintRole:
            return QtCore.QSize(20,20)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            item = self.getItem(index)
            result = item.setData(index.column(), value)
            if result:
                self.dataChanged.emit(index, index)
            self.puzzleInterface.updateGL()
            return result
        elif role == Qt.CheckStateRole:
            item = self.getItem(index)
            if item.isChecked():
                item.setCheckState(Qt.Unchecked)
                if item.itemData.enum == TTBase.enumType.CircleFactory:
                    for cf in item.itemData.circles:
                        cf.visible = False
                item.itemData.visible = False
            else:
                item.setCheckState(Qt.Checked)
                if item.itemData.enum == TTBase.enumType.CircleFactory:
                    for cf in item.itemData.circles:
                        cf.visible = True
                item.itemData.visible = True
            self.dataChanged.emit(index, index)
            self.puzzleInterface.updateGL()
            return True
        return False

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
        self.checked = Qt.Checked

    def child(self, row):
        try:
            return self.childItems[row]
        except IndexError:
            return None

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        '''What child index am I?'''
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return 2

    def data(self, column):
        dataArray = [self.itemData.label, self.itemData.value]
        return dataArray[column] #throws error if out of range

    def insertChildren(self, position, count, data):
        if position < 0 or position > len(self.childItems):
            return False
        for row in range(count):
            item = TreeItem(data, self)
            self.childItems.insert(position, item)
        return True

    def insertChild(self, position, data):
        if position < 0 or position > len(self.childItems):
            return False

        item = TreeItem(data, self)
        self.childItems.insert(position, item)
        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False
        for row in range(count):
            self.childItems.pop(position)
        return True

    def setData(self, column, value):
        if column == 0:
            self.itemData.label = value
            return True
        if column == 1:
            self.itemData.value = value
            return True
        return False

    def setCheckState(self,value):
        self.checked = value

    def isChecked(self):
        return self.checked


class PuzzleTreeView(QtGui.QTreeView):
    '''
    The view should have nothing to do with the puzzle
    It should only ask the model for things
    '''
    def __init__(self,parent):
        super(PuzzleTreeView,self).__init__(parent)
        self.setItemDelegate(TreeDelegate(self))
        self.header().setMovable(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self,pos):
        index = self.indexAt(pos)
        if not index.isValid():
            return
        item = index.internalPointer().itemData
        myMenu = QtGui.QMenu()

        if item.enum == TTBase.enumType.CircleFactory:
            self.factoryContext(index,item,myMenu,pos)
        elif item.enum == TTBase.enumType.Shell:
            self.shellContext(index,item,myMenu,pos)
        elif item.enum == TTBase.enumType.Graph:
            self.graphContext(index,item,myMenu,pos)
        elif item.enum == TTBase.enumType.Puzzle:
            self.puzzleContext(index,item,myMenu,pos)
        elif item.enum == TTBase.enumType.Sphere:
            self.sphereContext(index,item,myMenu,pos)

    def sphereContext(self,index,item,menu,pos):
        setMaterial = menu.addAction("Set Material")
        inheritMaterial = menu.addAction("Inherit Material")
        action = menu.exec_(self.mapToGlobal(pos))
        interface = self.model().puzzleInterface
        if action == setMaterial:
            r,g,b,a = QtGui.QColorDialog.getColor().getRgb()
            interface.materialObject(item, (r/255.0,g/255.0,b/255.0))
        elif action == inheritMaterial:
            interface.unmaterialObject(item)
        interface.fullUpdate()
        interface.updateGL()

    def puzzleContext(self,index,item,menu,pos):
        setColor = menu.addAction("Set Color")
        setMaterial = menu.addAction("Set Material")
        action = menu.exec_(self.mapToGlobal(pos))
        interface = self.model().puzzleInterface
        if action == setColor:
            r,g,b,a = QtGui.QColorDialog.getColor().getRgb()
            interface.colorObject(item, (r/255.0,g/255.0,b/255.0))
        if action == setMaterial:
            r,g,b,a = QtGui.QColorDialog.getColor().getRgb()
            interface.materialObject(item, (r/255.0,g/255.0,b/255.0))
        interface.fullUpdate()
        interface.updateGL()

    def factoryContext(self,index,item,menu,pos):
        addFactory = menu.addAction("Add Factory")
        delFactory = menu.addAction("Delete Factory")
        setColor = menu.addAction("Set Color")
        inheritColor = menu.addAction("Inherit Color")
        action = menu.exec_(self.mapToGlobal(pos))
        shell = index.parent().internalPointer().itemData
        interface = self.model().puzzleInterface
        if action == addFactory:
            interface.addFactory(shell)
            self.model().newFactory(index.parent(), interface.shellFactories(shell)[-1])
        elif action == delFactory:
            success = interface.removeFactory(item)
            if success:
                row = index.row()
                self.model().removeRows(row, 1, index.parent())
        elif action == setColor:
            r,g,b,a = QtGui.QColorDialog.getColor().getRgb()
            interface.colorObject(item, (r/255.0,g/255.0,b/255.0))
        elif action == inheritColor:
            interface.uncolorObject(item)
        interface.fullUpdate()
        interface.updateGL()
        flen = len(interface.shellFactories(shell))
        self.expandBranch(index.sibling(flen,0))

    def shellContext(self,index,item,menu,pos):
        copyShell = menu.addAction("Copy Shell")
        deleteShell = menu.addAction("Delete Shell")
        setMaterial = menu.addAction("Set Material")
        inheritMaterial = menu.addAction("Inherit Material")
        action = menu.exec_(self.mapToGlobal(pos))
        row = index.row()
        interface = self.model().puzzleInterface
        if action == copyShell:
            interface.copyShell(item)
            self.model().newShell(row+1,index.parent(),interface.puzzleShells()[row])
            interface.updateGL()
            self.expandBranch(index.sibling(row+1,0))
        elif action == deleteShell:
            success = interface.removeShell(item)
            if success:
                self.model().removeRows(row, 1, index.parent())
                interface.scene.updateGL()
        elif action == setMaterial:
            r,g,b,a = QtGui.QColorDialog.getColor().getRgb()
            interface.materialObject(item, (r/255.0,g/255.0,b/255.0))
        elif action == inheritMaterial:
            interface.unmaterialObject(item)

    def setModel(self,model):
        super(PuzzleTreeView,self).setModel(model)
        #I don't know why I have to expand the branch here
        #maybe because the view needs refreshed?
        self.expandBranch(model.index(0,0))

    def expandBranch(self,index):
        self.expand(index)
        childCount = index.internalPointer().childCount()
        for i in range(childCount):
            indexChild = index.child(i,0)
            self.expandBranch(indexChild)


class TreeDelegate(QtGui.QItemDelegate):
    def createEditor(self,parent,option,index):
        self.currentIndex = index
        item = index.internalPointer().itemData

        if index.column() == 1:
            if item.enum == TTBase.enumType.Symmetry:
                editor = QtGui.QComboBox(parent)
                editor.addItems(Symmetry.typeList)
                editor.setCurrentIndex(item.index)
                editor.currentIndexChanged.connect(self.updateSymmetry)
                return editor

            elif item.enum == TTBase.enumType.Value:
                if item.parents:
                    editor = QtGui.QDoubleSpinBox(parent)
                    if item.parents[0].enum == TTBase.enumType.CircleFactory:
                        editor.setRange(0.01,89.99)
                        editor.setSingleStep(1.00)
                        editor.valueChanged.connect(self.updateAngle)
                        return editor
                    elif item.parents[0].enum == TTBase.enumType.Sphere:
                        editor.setRange(0.01,10.00)
                        editor.setSingleStep(0.20)
                        editor.valueChanged.connect(self.updateThickness)
                        return editor
                    elif item.parents[0].enum == TTBase.enumType.Shell:
                        editor.setRange(0.01,2.00)
                        editor.setSingleStep(0.05)
                        editor.valueChanged.connect(self.updateThickness)
                        return editor


    def updateGeometry(self,editor,option,index):
        editor.setGeometry(option.rect)

    def setModelData(self, editor, model, index):
        pass #editing handled by signals

    def updateSymmetry(self,selectionIndex):
        symItem = self.currentIndex.internalPointer().itemData
        interface = self.currentIndex.model().puzzleInterface
        interface.changeSymmetry(symItem,selectionIndex)

    def updateAngle(self,angleValue):
        valItem = self.currentIndex.internalPointer().itemData
        interface = self.currentIndex.model().puzzleInterface
        interface.changeAngle(valItem.parents[0], angleValue)

    def updateRadius(self,radVal):
        valItem = self.currentIndex.internalPointer().itemData
        interface = self.currentIndex.model().puzzleInterface
        interface.changeRadius(valItem,radVal)

    def updateThickness(self,thickVal):
        valItem = self.currentIndex.internalPointer().itemData
        interface = self.currentIndex.model().puzzleInterface
        interface.changeRadius(valItem,thickVal)


