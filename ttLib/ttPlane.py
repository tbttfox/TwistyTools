#!/usr/bin/python
from __future__ import division

from ttPoint import TINYNUM,Point,dot,cross
from ttLine import Line
from ttBase import TTBase

class Plane(TTBase):
    def __init__( self,point=Point(),nrml=Point(1,0,0)):
        super(Plane,self).__init__()
        self.enum = self.enumType.Plane
        self.p = point
        self.n = nrml.n
        self.d = dot(self.n, self.p) #determinant
        self.setParents()

def pointDistPlane(point,plane):
    return dot(plane.n,(point - plane.p))
   
def pointOnPlane(point,plane):
    return -TINYNUM < pointDistPlane(point,plane) < TINYNUM

def planeIntPlane(Pn1, Pn2):
    v = cross(Pn1.n, Pn2.n).n #get the normalized vector of the line
    if v == Point(): #the planes are childallel
        return None
    
    #make absolute coords
    ax = abs(v[0])
    ay = abs(v[1])
    az = abs(v[2])

    mx0=2
    if ax>ay:
        if ax>az: mx0=0
    else:
        if ay>az: mx0=1
    mx1 = (mx0+1)%3
    mx2 = (mx0+2)%3
    d1 = Pn1.d
    d2 = Pn2.d

    #use a linear equasion to get the xyz coords of a point
    iP = [0,0,0]
    iP[mx1] = (d1*Pn2.n[mx2] - d2*Pn1.n[mx2]) / v[mx0]
    iP[mx2] = (d2*Pn1.n[mx1] - d1*Pn2.n[mx1]) / v[mx0]
    return Line(Point(*iP),v)



