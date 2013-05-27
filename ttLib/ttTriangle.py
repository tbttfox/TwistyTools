#!/usr/bin/python
from __future__ import division
from ttPoint import TINYNUM,Point,dot,cross,angle,distance
from ttBase import TTBase

class Triangle(TTBase):
    def __init__(self,p1,p2,p3):
        self.enum = TTBase.enumType.Triangle
        v1 = p2-p1
        v2 = p3-p1
        #zero if worldCenter lies on the same plane
        ng = dot(cross(v1,v2),p1)
        if -TINYNUM < ng < TINYNUM: 
            return None
        #make sure the triangle goes ccw 
        c1 = p1
        if ng > 0: c3,c2 = p2,p3
        else: c2,c3 = p2,p3

        self.p = [p1,p2,p3]
        self._a = None
        self._s = None
        self.parents = []
        self.setParents()

    @property
    def a(self):
        if self._a == None:
             self._a = [angle(self.p[1]-self.p[0], self.p[2]-self.p[0]),
                        angle(self.p[2]-self.p[1], self.p[0]-self.p[1]), 
                        angle(self.p[0]-self.p[2], self.p[1]-self.p[2])]
        return self._a

    @property
    def s(self):
        if self._s == None:
            self._s = [ distance(self.p[0], self.p[1]),
                        distance(self.p[1], self.p[2]),
                        distance(self.p[2], self.p[0])]
        return self._s

    def __eq__(self,other):
        if other.enum == self.enum:
            ms = Point(*self.s)
            p = other.s
            ys = [Point(p[0],p[1],p[2]), Point(p[1],p[2],p[0]), Point(p[2],p[0],p[1])]
            if ms in ys:
                return True
        return False

    @property
    def drawObject(self):
        return None

