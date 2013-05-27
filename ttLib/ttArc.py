#!/usr/bin/python
from __future__ import division
from math import pi,ceil,sin,cos,radians
from ttBase import TTBase
from ttPoint import TINYNUM,TINYANGLE,Point,cross,ccAngle,distance
from ttCircle import Circle,pointOnCircle

class Arc(TTBase):
    """ Don't worry about children/parents ... The arc is just a part of a region/shard """
    def __init__(self,start=Point(),end=Point(),center=Point()):
        super(Arc,self).__init__()
        self.enum = TTBase.enumType.Arc
        self.start = start
        self.end = end
        self.c = center
        self.r = distance(self.c,self.start)
        self._circle = None
        self.n = self.c.n
        self._midpoint = None
        self._ptList = None

    def __eq__(self,other):
        if other.enum == TTBase.enumType.Arc:
            if abs(self.r - other.r) < TINYNUM:
                if other.start == self.start: 
                    if other.end == self.end:
                        if other.c == self.c:
                            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Arc {0}>".format(id(self))

    @property
    def circle(self):
        if self._circle == None:
            self._circle = Circle(self.r,self.c)
        return self._circle

    @property
    def midpoint(self):
        if self._midpoint == None: 
            vm = ((self.start + self.end) / 2) - self.c
            vm = self.r * vm.n #vector to midpoint
            if ccAngle(self.start,self.c,self.end) > pi:
                self._midpoint =  self.c - vm
            else:
                self._midpoint =  self.c + vm
        return self._midpoint

    def subdivide(self,angleHint=10):
        if self._ptList == None:
            totalAngle = ccAngle(self.start,self.c,self.end) 
            numSteps = int(ceil(totalAngle / radians(angleHint)))
            step = totalAngle / numSteps
            yvec = (self.start - self.c).n
            xvec = cross(self.n, yvec).n
            self._ptList = []
            for i in range(numSteps):
                stepAngle = step * i
                xcomp = (sin(stepAngle) * xvec)
                ycomp = (cos(stepAngle) * yvec)
                self._ptList.append(((xcomp + ycomp) * self.r) + self.c)
            self._ptList.append(self.end)
        return self._ptList

    @property
    def drawObject(self):
        if self._drawObject == None:
            self._drawObject = DrawArc(self)
        return self._drawObject




def pointOnArc(P,A):
    if pointOnCircle(P,A.circle):
        if ccAngle(A.start, A.c, P) < ccAngle(A.start, A.c, A.end) - TINYANGLE:
            return True

def pointCutArc(P,A):
    if pointOnArc(P,A):
        return Arc(A.start,P,A.c), Arc(P,A.end,A.c)

def circleCutArc(C,A): #I could use pointOnArc, but this lets me re-use some variables
    possiblePoints = circleIntCircle(C,A.circle)
    if not possiblePoints: #if there's no intersection
        return None
    p1, p2 = possiblePoints
    se = ccAnlge(A.start, A.c, A.end) # Start/End angle
    sp1 = ccAngle(A.start, A.c, p1) # Start to Point1
    sp2 = ccAngle(A.start, A.c, p2) # Start to Point2
    if sp1 < se - TINYANGLE: # if p1 on A
        if sp2 < se - TINYANGLE: # if p2 on A
            if sp1 < sp2: #both on A, figure out the order
                return Arc(start, p1, A.c), Arc(p1, p2, A.c), Arc(p2, end, A.c)
            else:
                return Arc(start, p2, A.c), Arc(p2, p1, A.c), Arc(p1, end, A.c)
        else: #only p1 on A
            return Arc(A.start,p1,A.c), Arc(p1,A.end,A.c)
    elif sp2 < se - TINYANGLE: # if p2 on A
        return Arc(A.start,p2,A.c), Arc(p2,A.end,A.c)
    return None

def pointsCutCircle(pListRaw,C):
    pList = [p for p in pListRaw if pointOnCircle(p,C)]
    if len(pList) < 1:
        return None
    bp = pList[0] # base Point
    # get list of (angle, point) tuples
    apList = [ (ccAngle(bp, C.c, p),  p)  for p in pList]
    # sort tuples by angle 
    apList.sort(key=lambda x: x[0])
    return [Arc(apList[n-1][1], apList[n][1], C.c) for n in range(len(apList))]


