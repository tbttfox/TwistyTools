#!/usr/bin/python
from ttPoint import Point
from ttBase import TTBase
from ttValue import Value
from ttLine import lineIntSphere
from Draw.DrawSphere import DrawSphere

class Sphere(TTBase):
    def __init__(self,radius=1,center=Point()):
        super(Sphere,self).__init__()
        self.enum = self.enumType.Sphere
        self.label = "Sphere"
        self._r = Value(radius,"Radius")
        #polymorphic name used in shell stacks
        self.nextRad = radius
        self.c = center
        self.setParents()

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self,value):
        self._r.value = value

    @property
    def outrad(self):
        return self._r.value

    @property
    def children(self):
        return [self._r]

    @property
    def drawObject(self):
        if self._drawObject == None:
            self._drawObject = DrawSphere(self)
        return self._drawObject

    def getDrawState(self, drawState):
        if self.visible:
            ds = drawState.copy()
            if self.color:
                ds.color = self.color
            if self.material:
                ds.material = self.material
            ds.scale = self._r.value * ds.scale
            ds.drawObject = self.drawObject
            return [ds]
        return []
            




    def rayPick(self,ray):
        points = lineIntSphere(ray,self)
        if points is None:
            return []
        return [(points[0], self), (points[1], self)]


