#!/usr/bin/python

from PyQt4 import QtCore
from ttUI.warnings import warningMessage

from ttBase import TTBase
from ttSymmetry import Symmetry
from ttMkPuzzle import ShellSpec,puzzleFactory


class PuzzleInterface(QtCore.QObject):
    """
    This is here specifically to provide a layer between this and the puzzle
    It'll allow me to get information about the puzzle easily

    Also, it's here to provide gui signals so the puzzle itself doesn't
    have to worry about them at all
    """

    shellAdded = QtCore.pyqtSignal(object,int) #puzzle,newRow
    shellRemoved = QtCore.pyqtSignal(object,int) #puzzle,rowRemoved

    factoryAdded = QtCore.pyqtSignal(object) 
    factoryRemoved = QtCore.pyqtSignal(object,int) #shell, rowRemoved

    radiusChanged = QtCore.pyqtSignal(object)
    angleChanged = QtCore.pyqtSignal(object)
    symmetryChanged = QtCore.pyqtSignal(object)

    visibilityToggled = QtCore.pyqtSignal(object)
    objectColored = QtCore.pyqtSignal(object)

    puzzleDrawMode = 0
    pieceDrawMode = 1
    

    #eventually there will be picking signals here too


    def __init__(self, puzzle, parent=None):
        super(PuzzleInterface,self).__init__(parent)
        self.puzzle = puzzle
        self.scene = None
        self.drawMode = self.puzzleDrawMode

        #connect recursive updates
        self.shellAdded.connect( self.childRecursiveUpdate)
        self.shellRemoved.connect( self.childRecursiveUpdate)
        self.factoryAdded.connect( self.childRecursiveUpdate)
        self.factoryRemoved.connect( self.childRecursiveUpdate)
        self.radiusChanged.connect( self.childRecursiveUpdate)
        self.angleChanged.connect( self.childRecursiveUpdate)
        self.symmetryChanged.connect( self.childRecursiveUpdate)

        #connect single updates
        self.visibilityToggled.connect( self.singleObjectUpdate)
        self.objectColored.connect( self.singleObjectUpdate)


        self.radiusChanged.connect( self.puzzle.dirtyPieces)
        self.angleChanged.connect( self.puzzle.dirtyPieces)
        self.symmetryChanged.connect( self.puzzle.dirtyPieces)




    ###################
    ### INFORMATION ###
    ###################


    def itemParents(self,item): #default return []
        return item.parents

    def itemChildren(self,item): #default return []
        return item.children

    def puzzleShells(self):
        return self.puzzle.shellList

    def shellFactories(self,shell):
        return shell.factoryList


    ###############
    ### ACTIONS ###
    ###############

    def copyShell(self, shell=None, row=None):
        if row is None:
            row = self.puzzle.shellList.index(shell)
        self.puzzle.copyShell(row)
        self.shellAdded.emit(self.puzzle,row)

    def removeShell(self, shell=None, row=None):
        if len(self.puzzle.shellList) <= 1:
            warningMessage("One shell to rule them all")
            #I should probably raise an exception instead
            return False

        if row is None:
            row = self.puzzle.shellList.index(shell)
        self.puzzle.deleteShell(row)
        self.shellRemoved.emit(self.puzzle,row)
        return True
            
    def addFactory(self, shell):
        shell.copyLastFactory()
        self.factoryAdded.emit(shell)

    def removeFactory(self, factory=None, row=None):
        shell = factory.parents[0]
        if len(shell.factoryList) <= 1:
            warningMessage("One factory to find them")
            return False
        row = shell.factoryList.index(factory)
        shell.deleteFactory(row)
        self.factoryRemoved.emit(shell,row)
        return True

    def changeRadius(self, thing, newrad): 
        par = thing.parents[0]
        if par.enum == TTBase.enumType.Sphere:
            par.r = newrad
            self.radiusChanged.emit(thing)
        elif par.enum == TTBase.enumType.Shell:
            par.thickness = newrad
            self.radiusChanged.emit(thing)

    def changeAngle(self, factory, value):
        factory.angle = value
        self.angleChanged.emit(factory)

    def changeSymmetry(self, symmetry, index):
        symmetry.index = index
        self.symmetryChanged.emit(symmetry)

    def toggleVisibility(self, thing):
        if thing.visible == True:
            self.hideObject(thing)
        else:
            self.revealObject(thing)

    def colorObject(self, thing, color): #color is (rgb) floats from 0 to 1
        thing.color = color
        self.objectColored.emit(thing)

    def uncolorObject(self, thing):
        if not thing.inheritsColor():
            thing.inheritColor()
            self.objectColored.emit(thing)

    def materialObject(self, thing, material):
        thing.material = material
        self.objectColored.emit(thing)

    def unmaterialObject(self, thing):
        if not thing.inheritsMaterial():
            thing.inheritMaterial()
            self.objectColored.emit(thing)

    def hideObject(self,thing):
        if thing.visible == True:
            thing.visible = False
            self.visibilityToggled.emit(thing)

    def revealObject(self,thing):
        if thing.visible == False:
            thing.visible = True
            self.visibilityToggled.emit(thing)

    def hideAll(self):
        def recHide(item):
            item.visible = False
            for child in item.children:
                recHide(child)
        recHide(self.puzzle)
        self.visibilityToggled.emit(self.puzzle)

    def revealAll(self):
        def recReveal(item):
            item.visible = True
            for child in item.children:
                recReveal(child)
        recReveal(self.puzzle)
        self.visibilityToggled.emit(self.puzzle)

    def childRecursiveUpdate(self,thing,nullArg=None):
        thing.dirtyParents()
        thing.bfUpdate()
        self.updateGL()

    def singleObjectUpdate(self,thing,nullArg=None):
        thing.cleanup()
        self.updateGL()

    def updateGL(self):
        if self.scene:
            self.scene.updateGL()

    def fullUpdate(self,*args):
        self.childRecursiveUpdate(self.puzzle)

    def setScene(self,scene):
        self.scene = scene

    def rayPick(self,ray):
        self.puzzle.rayPick(ray)

    def draw(self):
        if self.drawMode == self.puzzleDrawMode:
            ds = self.puzzle.getDrawState()
            for d in ds:
                d.drawObject.draw(d)
        elif self.drawMode == self.pieceDrawMode:
            ds = self.puzzle.getDrawState()
            for d in ds:
                d.drawObject.draw(d)




