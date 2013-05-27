#!/usr/bin/python
from ttCircle import Circle
from ttBase import TTBase,DrawState
from ttValue import Value
from math import sin,cos,radians
from Draw.DrawCut import DrawCut
from ttCone import lineIntCone

class CircleFactory(TTBase):
    def __init__(self,angle,symmetry):
        super(CircleFactory,self).__init__()
        self.enum = self.enumType.CircleFactory
        self.label = "Cut Generator"
        self._symmetry = symmetry
        self._angle = Value(angle,"Angle")
        self._circles = None
        self._drawCuts = None
        self.setParents()

    @property
    def circles(self):
        if self._circles == None:
            self._circles = []
            h = cos(radians(self._angle.value))
            rad = sin(radians(self._angle.value))
            self._circles = [Circle(rad, axis.n*h) for axis in self.symmetry]
        return self._circles

    def cleanup(self):
        self._circles = None
        self._drawCuts = None
        self.setParents()

    @property 
    def symmetry(self):
        return self._symmetry

    @symmetry.setter
    def symmetry(self,symmetry):
        self._symmetry = symmetry
        self._circles = None

    @property
    def children(self):
        return [self._angle,self.symmetry] 

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self,value):
        self._angle.value = value
        h = cos(radians(self._angle.value))
        rad = sin(radians(self._angle.value))
        for c in self.circles:
            c.setRadHeight(rad,h)
        
    @property
    def cuts(self):
        if self._drawCuts is None:
            self._drawCuts = DrawCut(self)
        return self._drawCuts

    def clone(self):
        ang = self.angle.value
        sym = self.symmetry.clone()
        return CircleFactory(ang,sym)

    def rayPick(self,ray,inrad,outrad):
        #hit all conical cut sides
        hits = []
        for c in self.circles:
            pts = lineIntCone(ray,c)
            if pts:
                for pt in pts:
                    if inrad**2 < pt.abs2 < outrad**2:
                        hits.append( (pt,self) )
        return hits

    def getDrawState(self, drawState):
        ds = drawState.copy()
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material
        states = []
        if self.visible:
            for c in self.circles:
                states.extend(c.getDrawState(ds))
        return states        

    def getCutsDrawState(self,drawState):
        if self.visible:
            ds = drawState.copy()
            if self.color:
                ds.color = self.color
            if self.material:
                ds.material = self.material
            ds.drawObject = self.cuts
            return [ds]
        return []

