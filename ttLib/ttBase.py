#!/usr/bin/python
from copy import deepcopy

class TTBase(object):
    value = ""
    drawObject = None

    class enumType:
        Point = 0
        Symmetry = 1
        Sphere = 2
        Line = 3
        Plane = 4
        Circle = 5
        Arc = 6
        Region = 7
        Triangle = 8
        Graph = 9
        Shell = 10
        Shard = 11
        Piece = 12
        Puzzle = 13
        CircleFactory = 14
        Value = 15

    def __init__(self):
        self.parents = []
        self.scene = None
        self.dirty = False
        self.visible = True
        self.label = ""
        self._drawObject = None
        self._color = None
        self._material = None
        self.defaultColor = (0,1,0)
        self.defaultMaterial = (0.5, 0.5, 0.5)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self,rgb):
        self._color = (rgb[0], rgb[1], rgb[2])

    def inheritsColor(self):
        if self._color == None:
            return True
        return False

    def inheritColor(self):
        self._color = None

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self,rgb):
        self._material = (rgb[0], rgb[1], rgb[2])

    def inheritsMaterial(self):
        if self._material == None:
            return True
        return False

    def inheritMaterial(self):
        self._material = None

    def cleanup(self):
        pass

    def recursiveParents(self):
        ret = []
        childs = self.children
        if childs:
            for p in self.children:
                ret.extend(p.recursiveParents())
        else:
            childs = []
        childs.extend(ret)
        return childs

    def bfUpdate(self): #bredth first update
        inpile = [self]
        while inpile:
            node = inpile.pop(0)
            if node.dirty:
                inpile.extend(node.parents)
                node.cleanup()
                node.dirty = False

    def dirtyParents(self):
        self.dirty = True
        for parent in self.parents:
            parent.dirtyParents()

    def setParents(self):
        if self.children:
            for item in self.children:
                if self not in item.parents:
                    item.parents.append(self)

    def fullUpdate(self):
        for child in self.children:
            child.fullUpdate()
        self.cleanup()         
    
    def getRoot(self):
        if self.parents:
            return self.parents[0].getRoot()
        return self

    @property
    def children(self):
        return []

    def getDrawState(self, drawState):
        ds = deepcopy(drawState)
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material
        ds.drawObject = self.drawObject
        return [ds]
        
class DrawState(object):
    def __init__(self):
        self.color = (0, 1, 0)
        self.material = (0.5, 0.5, 0.5)
        self.scale = 1
        self.inrad = 1
        self.outrad = 1.2
        self.drawObject = None

    def copy(self):
        return deepcopy(self)
    

