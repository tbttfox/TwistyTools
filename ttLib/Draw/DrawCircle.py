#!/usr/bin/python
from __future__ import division
from math import pi,sin,cos,degrees
from ttLib.ttPoint import TINYNUM,Point,cross,ccAngle
from DrawBase import DrawBase
from OpenGL.GL import *

class DrawCircleVerts(object):
    n = 96
    pi2n = 2 * pi / n
    verts = [Point(cos(pi2n * i), sin(pi2n * i), 0) for i in range(n)]


class DrawCircle(DrawBase):
    def __init__(self,*args,**kwargs):
        super(DrawCircle,self).__init__(*args,**kwargs)
        self.getRotAxis()
        self.glVerts = DrawCircleVerts.verts

    def getRotAxis(self):
        if (-TINYNUM < self.thing.c[0] < TINYNUM) and (-TINYNUM < self.thing.c[1] < TINYNUM):
            self.axis = Point(1, 0, 0)
            if self.thing.c[2] < 0:
                self.angle = pi 
            else:
                self.angle = 0
        else:
            self.axis = cross(Point(0,0,1), self.thing.c).n
            self.angle = ccAngle(Point(0,0,1), Point(), self.thing.c)

    @property
    def glID(self):
        if self._glID == None:
            self._glID = glGenLists(1)
            glNewList(self._glID,GL_COMPILE)
            glDisable(GL_LIGHTING)
            glLineWidth(self.size)
            glBegin(GL_LINE_STRIP)
            for vert in self.glVerts:
                glVertex3f(*vert)
            glVertex3f(*self.glVerts[0])
            glEnd()
            glEndList()
        return self._glID

    def draw(self,ds):
        scale = ds.scale
        color = ds.color
        glPushMatrix()
        glColor3f(*color)
        glScalef(scale, scale, scale)
        glRotatef(degrees(self.angle),*self.axis)
        glTranslate(0,0,self.thing.h)
        glScalef(self.thing.r, self.thing.r, 1)
        glCallList(self.glID)
        glPopMatrix()



