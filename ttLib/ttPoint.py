#!/usr/bin/python
from __future__ import division
from math import acos,atan2,pi
from ttBase import TTBase
from Draw.DrawPoint import DrawPoint
from decimal import Decimal

TINYNUM = 0.0000000001
TINYANGLE = 0.0000001

class Point(TTBase):
    def __init__(self,x=None,y=None,z=None):
        super(Point,self).__init__()
        self._n = None
        self._abs2 = None
        self._abs = None
        self.enum = self.enumType.Point
        if x == None:
            self._p = (0.0, 0.0, 0.0)
        else:
            self._p = (float(x),float(y),float(z))
        self.setParents()

    def __iter__(self):
        for i in self._p:
            yield i

    def __str__(self):
        nums = ','.join([str(i) for i in self._p])
        return "Point(" + nums + ")"

    def __repr__(self):
        nums = ','.join([str(i) for i in self._p])
        return "<ttPoint.Point(" + nums + ")>"

    def __eq__(self,right):
        if right.__class__ == Point:
            if -TINYNUM < (self._p[0] - right._p[0]) < TINYNUM:
                if -TINYNUM < (self._p[1] - right._p[1]) < TINYNUM:
                    if -TINYNUM < (self._p[2] - right._p[2]) < TINYNUM:
                        return True
            return False
        return NotImplemented

    def __ne__(self,right):
        return not self.__eq__(right)

    def __neg__(self):
        return Point(-1*self._p[0], -1*self._p[1], -1*self._p[2])

    def __getitem__(self,key):
        return self._p[key]

    @property
    def n(self):
        if self._n == None:
            den = abs(self)
            if den < TINYNUM: 
                self._n = Point()
            else: 
                self._n = Point(*[i/den for i in self._p])
        return self._n

    @property
    def p(self):
        return self._p
    @p.setter
    def p(self,value):
        self._abs2 = None
        self._abs = None
        self._n = None
        self._p = tuple(map(float,value))

    @property
    def abs2(self):
        if self._abs2 == None:
            self._abs2 = sum([i**2 for i in self._p])
        return self._abs2
    def __abs__(self):
        if self._abs == None:
            self._abs = self.abs2 ** .5
        return self._abs
        
    def __add__(self,right): 
        if right.__class__ == Point:
            return Point(self._p[0]+right.p[0],self._p[1]+right.p[1],self._p[2]+right.p[2])

    def __sub__(self,right): 
        if right.__class__ == Point:
            return Point(self._p[0]-right.p[0],self._p[1]-right.p[1],self._p[2]-right.p[2])

    def __div__(self,right): 
        try:
            fright = float(right)
            return Point(self._p[0]/fright,self._p[1]/fright,self._p[2]/fright)
        except:
            return NotImplemented
    def __mul__(self,right): 
        try:
            fright = float(right)
            return Point(self._p[0]*fright,self._p[1]*fright,self._p[2]*fright)
        except:
            return NotImplemented

    def __rmul__(self,left):
        return self.__mul__(left)

    def __truediv__(self,right):
        return self.__div__(right)

    @property
    def drawObject(self):
        if self._drawObject == None:
            self.drawObject = DrawPoint(self) 
        return self._drawObject



def dot(a,b):
    return (a.p[0]*b.p[0]+a.p[1]*b.p[1]+a.p[2]*b.p[2])

def cross(a,b):
    nx = (a.p[1]*b.p[2] - a.p[2]*b.p[1]) 
    ny = (a.p[2]*b.p[0] - a.p[0]*b.p[2]) 
    nz = (a.p[0]*b.p[1] - a.p[1]*b.p[0])
    return Point(nx,ny,nz)

def matMul(p,mat):
    nx = (mat[0][0] * p.p[0]+ mat[0][1] * p.p[1]+ mat[0][2] * p.p[2]+ mat[0][3])
    ny = (mat[1][0] * p.p[0]+ mat[1][1] * p.p[1]+ mat[1][2] * p.p[2]+ mat[1][3])
    nz = (mat[2][0] * p.p[0]+ mat[2][1] * p.p[1]+ mat[2][2] * p.p[2]+ mat[2][3])
    return Point(nx,ny,nz)

def ccAngle(start,center,end): #counterClockwise angle
    a = (start-center)
    b = (end-center)
    ang = angle(start,center,end)
    if dot(cross(a,b),center) > 0:
        return ang % (2*pi)
    else:
        return ((2*pi) - ang) % (2*pi)

def angle(start,center,end):
    if start == center or end == center:
        return 0
    a = (start-center).n
    b = (end-center).n
    d = dot(a,b)
    if -1 > d or d > 1: 
        #make sure float errors don't kill the acos operation
        d = int(d)
    return acos( d )

def distance2(a,b):
    return (a-b).abs2

def distance(a,b):
    return abs(a-b)

#convert cartesian coords to uv
def cart2uv(p):
    r2 = p.abs2
    if r2 > 0:
        u = atan2(p[0],p[2]) / (2*pi)
        v = acos(p[1]/r2**0.5) / (2*pi)
        if u < 0:
            u = u + 1
        return u,v
    else:
        return 0,0




#get an axis/angle to rotate +Z unit vector to arbitrary unit vector


def getRotAxis(p):
    if (-TINYNUM < p[0] < TINYNUM) and (-TINYNUM < p[1] < TINYNUM):
        axis = Point(1, 0, 0)
        if p[2] < 0:
            angle = pi 
        else:
            angle = 0
    else:
        axis = cross(Point(0,0,1), p).n
        angle = ccAngle(Point(0,0,1), Point(), p)

    return axis, angle








