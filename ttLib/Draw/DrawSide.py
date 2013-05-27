#!/usr/bin/python
from DrawBase import DrawBase
from OpenGL.GL import *

class DrawSide(DrawBase):
    def __init__(self,*args,**kwargs):
        super(DrawSide,self).__init__(*args,**kwargs)
        self.inrad = None
        self.outrad = None

    @property
    def glID(self):
        if self._glID == None:
            pn = (self.thing.posneg * 2) - 1
            arcPoints = self.thing.arc.subdivide(angleHint=10)
            arcNormals = [(self.thing.arc.c - ap)*pn for ap in arcPoints]
            self._glID = glGenLists(1)
            glNewList(self._glID,GL_COMPILE)
            glBegin(GL_TRIANGLE_STRIP)
            for i in range(len(arcPoints)):
                glNormal3f(*arcNormals[i])
                glVertex3f(*(arcPoints[i] * self.inrad))
                glVertex3f(*(arcPoints[i] * self.outrad))
            glEnd()
            glEndList()
        return self._glID
            

    def draw(self,ds):
        if ds.inrad != self.inrad or ds.outrad != self.outrad:
            #update the object  any time the radii change
            self.inrad = inrad
            self.outrad = outrad
            if self._glID:
                glDeleteLists(self._glID,1)
                self._glID = None
        scale = ds.scale
        material = ds.material
        glPushMatrix()
        glScalef(self.scale, self.scale, self.scale)
        glCallList(self.glID)
        glPopMatrix()


