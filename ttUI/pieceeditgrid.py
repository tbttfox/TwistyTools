#!/usr/bin/python
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from warnings import warningMessage

#http://pepper.troll.no/s60prereleases/doc/itemviews-addressbook.html


class GridItem(object):
    '''
    This clas will eventually find a quick pixmap render of each shard
    and set that pixmap to be an icon for each piece
    But until then, I just need to change its color
    '''
    falseBrush = QtGui.QBrush(QtGui.QColor("white"))
    trueBrush = QtGui.QBrush(QtGui.QColor("red"))
    def __init__(self,data=None,parent=None):
        self.parentItem = parent
        self.itemData = data

    def data(self):
        if self.itemData:
            return self.trueBrush
        else:
            return self.falseBrush

    def setData(self,val):
        self.itemData = val
        

#my editable table model
class GridModel(QtCore.QAbstractTableModel):
    def __init__(self, puzzle, parent=None):
        super(GridModel, self).__init__(parent)
        self.puzzle = puzzle
        self.setDataArray()

    def setDataArray(self):
        pieces = self.puzzle.puzzle.pieces
        shells = self.puzzle.puzzleShells()
        self.dataArray = [[GridItem()]]
        self.insertRows(0,len(shells)-1)
        self.insertColumns(0,len(pieces)-1)
        for shellNum,shell in enumerate(shells):
            for pieceNum,piece in enumerate(pieces):
                for reg in piece:
                    if reg in shell.regions:
                        self.dataArray[shellNum][pieceNum].setData(reg)

    def rowCount(self,parent=None):
        #return len(self.puzzle.puzzleShells())
        return len(self.dataArray)

    def columnCount(self,parent=None):
        if self.dataArray != []:
            return len(self.dataArray[0])
        return 0

    def data(self,index,role):
        if not index.isValid():
            return None
        if index.row() - 1 > self.rowCount() or index.row() < 0 :
            return None
        if index.column() - 1 > self.columnCount() or index.column() < 0 :
            return None

        if role in (Qt.DisplayRole, Qt.EditRole):
            return "Test"
            #item = self.getItem(index)
        elif role == Qt.BackgroundRole:
            item = self.getItem(index)
            return item.data()

    def getItem(self,index):
        '''self.dataArray[row][column]'''
        return self.dataArray[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return "Piece {0}".format(section+1)
        if orientation == Qt.Vertical:
            return "Shell {0}".format(section+1)
        return None

    def insertRows(self, position, count, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for c in range(count):
            newrow = [GridItem() for i in self.dataArray[0]]
            self.dataArray.insert(position,newrow)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for c in range(count):
            self.dataArray.pop(position)
        self.endRemoveRows()
        return True

    def insertColumns (self, position, count, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent,position, position+count-1)
        for i,row in enumerate(self.dataArray):
            newItems = [GridItem() for x in range(count)]
            newrow = row[:position] + newItems + row[position:]
            self.dataArray[i] = newrow
        self.endInsertColumns()
        return True

    def removeColumns (self, position, count, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent,position, position+count-1)
        for i,row in enumerate(self.dataArray):
            newrow = row[:position] + row[position+count:]
            self.dataArray[i] = newrow
        self.endRemoveColumns()
        return True

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            return True
            
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return  Qt.ItemIsEditable | Qt.ItemIsEnabled

    def refreshDataArray(self):
        """Pare the whole array down to a 1x1 and reset the bastard"""
        self.removeRows(0, self.rowCount()-1)
        self.removeColumns(0, self.columnCount()-1)
        self.setDataArray()


class PieceEditGrid(QtGui.QTableView):
    def __init__(self,parent):
        super(PieceEditGrid,self).__init__(parent)
        self.test = 1

    def registerPuzzle(self,puzzle):
        self.puzzle = puzzle
        model = GridModel(self.puzzle)
        self.setModel(model)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self,pos):
        myMenu = QtGui.QMenu()
        self.extraContext(myMenu, pos)

    def extraContext(self, menu, pos):
        resetAction = menu.addAction("Reset")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == resetAction:
            self.refreshGrid()

    def refreshGrid(self):
        self.model().refreshDataArray()
        




#switch to piece mode
#On switch,  calculate all pieces
#
#When a filled box is selected on a grid
    #show wireframe for all shards in piece
    #show solid for current shard
    #This should work for all the cases I want to deal with
#
#
#ability to swap a specific shard for a new one
#ability to remove a shard
#ability to add a shard
#
#ability to create a new piece (column)
#
#
#
#On shardSwap
    #need toggles for shell visibility
    #use selection to pick a 
    
    
    



