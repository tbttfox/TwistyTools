#!/usr/bin/python
from __future__ import division
from ttLib.ttPoint import TINYNUM,Point,cross,matMul,angle,cart2uv
from DrawBase import DrawBase
from OpenGL.GL import *
from OpenGL.GLU import *
from math import pi,cos,sin,degrees,radians
from copy import copy


class DrawRegion(DrawBase):
    def __init__(self,*args,**kwargs):
        super(DrawRegion,self).__init__(*args,**kwargs)
        self.resolution = 1
        self.nurbInit()
        self.trimInit()

    def nurbInit(self):
        deg = 3
        uSides = 16
        vSides = uSides * 2
        w = 1.0064 #fixes the fact that the cubic curves aren't tangent to the control poly
        vAngles = [t * pi * 2 / vSides for t in range(-1,vSides+2)]
        uAngles = vAngles[:uSides+deg]
        uCurve = [(cos(a) * w,  sin(a) * w) for a in uAngles]
        self.cvs = [[[sin(vA)*uCurve[i][1]*w, uCurve[i][0], cos(vA)*uCurve[i][1]*w] 
                for vA in vAngles] for i in range(len(uCurve))]
        self.vKnots = range(len(self.cvs[0]) + deg + 1)
        self.uKnots = range(len(uCurve) + deg + 1)
        self.nurb = gluNewNurbsRenderer()
        gluNurbsProperty(self.nurb, GLU_SAMPLING_METHOD,GLU_DOMAIN_DISTANCE)
        gluNurbsProperty(self.nurb, GLU_U_STEP,self.resolution)
        gluNurbsProperty(self.nurb, GLU_V_STEP,self.resolution)
        gluNurbsProperty(self.nurb, GLU_CULLING,True)

    def trimInit(self):
        rawTrim = []
        for a,d in zip(self.thing.arcs,self.thing.posNeg): #*A*rc and *D*irection
            vertCopy = copy(a.subdivide())
            if d != 0:
                vertCopy.reverse()
            rawTrim.append(vertCopy)
        centroid = self.thing.center #get the centroid of all the corners
        nzAxis = Point(0,0,-1)
        rotAxis = cross(centroid, nzAxis) #cross that vector with -z to get a rotation axis
        if rotAxis.abs2 < TINYNUM:
            rotAxis = Point(1,0,0)
        rotAngle = angle(centroid,Point(),nzAxis) #get the angle between the vectors
        glPushMatrix() #get rotation axis
        glLoadIdentity()
        glRotatef(degrees(-1 * rotAngle),*rotAxis)
        self.invrotMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix() 
        uv2 = [[cart2uv(matMul(Point(*x), self.invrotMatrix)) for x in a] for a in rawTrim]
        self.trimVerts = [[(x[1]*32+3,x[0]*32+3) for x in a] for a in uv2]

    @property
    def glID(self):
        if self._glID == None:
            self.nurbInit()
            self.trimInit()
            self._glID = glGenLists(1)
            x2uv = []
            for x in self.trimVerts: 
                x2uv = x2uv + x
            glNewList(self._glID,GL_COMPILE)
            gluNurbsProperty(self.nurb, GLU_DISPLAY_MODE, GLU_FILL)
            gluBeginSurface(self.nurb)
            gluNurbsSurface(self.nurb,self.uKnots,self.vKnots,self.cvs,GL_MAP2_VERTEX_3)

            gluBeginTrim(self.nurb)
            gluPwlCurve(self.nurb, x2uv, GLU_MAP1_TRIM_2 )
            gluEndTrim(self.nurb)

            gluEndSurface(self.nurb)
            glEndList()
        return self._glID

    def draw(self,ds):
        scale = ds.scale
        material = ds.material
        glLineWidth(self.size)
        glPushMatrix()
        glColor3f(*material)
        glScalef(scale,scale,scale)
        glMultMatrixf(self.invrotMatrix)
        glCallList(self.glID)
        glPopMatrix()



