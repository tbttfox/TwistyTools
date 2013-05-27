#!/usr/bin/python
from math import degrees
from DrawBase import DrawBase
from DrawCircle import DrawCircleVerts
from ttLib.ttPoint import Point,getRotAxis,cross
from OpenGL.GL import *

class DrawCut(DrawBase):
    #takes a circleFactory as the thing
    def __init__(self,*args,**kwargs):
        super(DrawCut,self).__init__(*args,**kwargs)
        self.glVerts = DrawCircleVerts.verts
        self.inrad = None
        self.outrad = None
        self.angle = self.thing.angle.value

    def generateCut(self,cf):
        #this is only for one circleFactory in the graph of the shell
        radius = cf.circles[0].r
        height = cf.circles[0].h
        hpoint = Point(0,0,height)
        baseCircle = [(v * radius) + hpoint for v in self.glVerts]
        incircle = [x * self.inrad for x in baseCircle]
        outcircle = [x * self.outrad for x in baseCircle]
        return incircle, outcircle

    def instantiateCut(self,symmetry,incircle,outcircle):
        for p in symmetry:
            axis, angle = getRotAxis(p)
            glPushMatrix()
            glRotatef(degrees(angle),*axis)
            glBegin(GL_TRIANGLE_STRIP)
            z = Point(0,0,1)
            for inPoint,outPoint in zip(incircle,outcircle):
                normal = cross(inPoint, cross(z, inPoint))
                glNormal3f(*normal)
                glVertex3f(*inPoint)
                glVertex3f(*outPoint)
            normal = cross(inPoint, cross(z, inPoint))
            glNormal3f(*normal)
            glVertex3f(*incircle[0])
            glVertex3f(*outcircle[0])
            glEnd()
            glPopMatrix()

    @property 
    def glID(self):
        if self._glID == None:
            self._glID = glGenLists(1)
            glNewList(self._glID,GL_COMPILE)
            incircle, outcircle = self.generateCut(self.thing)
            self.instantiateCut(self.thing.symmetry, incircle, outcircle)
            glEndList()
        return self._glID

    def draw(self,ds):
        scale = ds.scale
        inrad = ds.inrad
        outrad = ds.outrad
        material = ds.material

        #this object depends on both a shell and a single circle factory
        #This is what they were warning against when they say "Tightly coupled"
        if self.angle != self.thing.angle.value or inrad != self.inrad or outrad != self.outrad:
            #update the object  any time the angle or radius changes
            self.inrad = inrad
            self.outrad = outrad
            self.angle = self.thing.angle.value
            if self._glID:
                glDeleteLists(self._glID,1)
                self._glID = None
        glEnable(GL_LIGHTING)
        glColor3f(*material)
        glPushMatrix()
        glScale(scale,scale,scale)
        glCallList(self.glID)
        glPopMatrix()


