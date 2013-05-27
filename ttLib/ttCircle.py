#!/usr/bin/python
from __future__ import division
import sys
from math import pi,sin,cos,degrees
from ttPoint import TINYNUM,Point,dot,cross,distance2,ccAngle
from ttLine import pointProjectLine,pointOnLine
from ttPlane import Plane,planeIntPlane
from ttBase import TTBase
from Draw.DrawCircle import DrawCircle

class Circle(TTBase):
    def __init__(self,radius=1,center=Point()):
        super(Circle,self).__init__()
        self.enum = self.enumType.Circle
        self._r = radius
        self._c = center
        self.n = self._c.n
        self.h = abs(self._c)
        self.setParents()
        self.label = "Circle"

    def __hash__(self):
        #Ok,  so I need to have hashable circles for use in the region finder
        #I'll just hash the rounded tuple of the center point, rounded to TINYANGLE = 0.0000001 -> 7 digits
        #yeah, it's slow.  I'd just prefer it to be stable
        return hash((round(self.c[0],5), round(self.c[1],5), round(self.c[2],5)))

    def __repr__(self):
        #return "<ttCircle.Circle r:"+ str(self._r)+ " c:"+ str(self._c)
        return "<Circle {0}>".format(id(self))

    def __eq__(self,other):
        try:
            if other.enum == self.enumType.Circle:
                if -TINYNUM < self.r - other.r < TINYNUM:
                    if self.c == other.c:
                        return True
        except:
            return False

    def toPlane(self):
        return Plane(self.c,self.n)

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self,radius):
        """Setter for the radius
        This will also re-set the center point
        that way the circle will stay on its sphere"""
        # circles are always on a sphere with radius 1
        newCenterLen = (1 - (radius*radius)) ** .5
        self._c = self.n * newCenterLen
        self._r = radius    
        self.h = newCenterLen

    def setRadHeight(self,radius,height):
        """ Allows me to pre-compute radius and height
            so I don't have to use a lot of sqrt()
            assert: radius**2 + height**2 = 1 """
        self._r = radius
        self._c = self.n * height
        self.h = height

    @property
    def c(self):
        return self._c
    @c.setter
    def c(self,center):
        """Setter for the center
        This will also re-set the radius
        that way the circle will stay on its sphere"""
        sphereRad2 = (self.r*self.r) + (self.c.abs2())
        self._r = (sphereRad2 - center.abs2()) ** .5
        self._c = center
        self.n = self._c.n
        self.h = abs(self._c)

    @property
    def drawObject(self):
        if self._drawObject == None:
            self._drawObject = DrawCircle(self)
        return self._drawObject



def pointOnCircle(p,c):
    v = p-c.c #vector from center to point
    if -TINYNUM < dot(c.n, v) < TINYNUM: #if it's on the same plane
        return -TINYNUM < (v.abs2 - c.r**2) < TINYNUM
    return False

def circleIntPlane(C,P):
    iline = planeIntPlane(C.toPlane(),P)
    return lineIntCircle(iline,C)

def lineIntCircle(L,c):
    if -TINYNUM < dot(L.v, c.n) < TINYNUM: #They're in the same plane
        if pointOnLine(c.c,L): #the line goes through the center
            pm = c.r * L.v.n() #make vec along line, length radius
            return c.c + pm , c.c - pm
        else:
            proj = pointProjectLine(c.c, L) #get closest point on line to center
            cr2 = c.r**2 
            d2 = distance2(proj, c.c) 
            if d2 < cr2-TINYNUM: #only care if we have 2 intercepts
                #make vec along line half length of chord
                pm = ((cr2 - d2)**.5) * L.v.n 
                return proj+pm , proj-pm
    return None

def circleIntCircle(A,B):
    ap = A.toPlane()
    bp = B.toPlane()
    iLine = planeIntPlane(A.toPlane(),B.toPlane())
    if iLine == None: #the circles are childallel
        return None
    Aps = lineIntCircle(iLine,A)
    Bps = lineIntCircle(iLine,A)
    if Aps == None or Bps == None:
        return None

    if Aps[0] == Bps[0]:
        if Aps[1] == Bps[1]:
            return Aps[0], Aps[1]
    elif Aps[0] == Bps[1]:
        if Aps[1] == Bps[0]:
            return Aps[0], Aps[1]
    return None









