#!/usr/bin/python
from __future__ import division
from ttPoint import TINYNUM,Point,dot
from ttBase import TTBase
from Draw.DrawLine import DrawLine

class Line(TTBase):
    def __init__(self,point=Point(),vec=Point(1,0,0)):
        super(Line,self).__init__()
        self.enum = self.enumType.Point
        self.s = point #start
        self.v = vec #vector
        self.setParents()

    @property
    def drawObject(self):
        if self._drawObject == None:
            self._drawObject = DrawLine(self)
        return self._drawObject

def pointProjectLine(pt,L):
    return (dot(pt - L.s, L.v.n) * L.v.n) + L.s

def pointOnLine(pt,L):
    return pt == pointProjectLine(pt,L)

def lineIntLine(L1,L2):
    #http://www.softsurfer.com/Archive/algorithm_0106/algorithm_0106.htm
    w = L1.s - L2.s
    a = dot(L1.v, L1.v) #L1.v.abs2
    b = dot(L1.v, L2.v)
    c = dot(L2.v, L2.v) #L2.v.abs2
    d = dot(L1.v, w)
    e = dot(L2.v, w)
    D = a*c - b*b #definition <= 0
    if D < TINYNUM: #the lines are parallel
        return None

    sc = (b*e - c*d) / D
    tc = (a*e - b*d) / D
    #distance between lines at closest point
    dist = abs(w + (sc * L1.v) - (tc * L2.v)) 

    #if that connecting line is within tolerance
    if dist > TINYNUM:
        return None

    p1 = (sc * L1.v) + L1.s
    p2 = (tc * L2.v) + L2.s
    #average the close points and return that
    return (p1 + p2) / 2


def lineIntSphere(L,s):
    #project the sphere center onto the line
    proj = pointProjectLine(s.c,L)
    p2L = proj - s.c #pointToLine
    d2 = p2L.abs2 #height squared
    rad2 = s.r.value ** 2 #radius squared
    if d2 > rad2:
        return None #line is skew to sphere
    base =  (rad2 - d2)**0.5
    #now that we have a base length and a point,
    #normalize the line's vector and multiply by
    # +/- base and add to the projected point
    return (proj + L.v.n*base,  proj - L.v.n*base)





    

