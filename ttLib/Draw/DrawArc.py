#!/usr/bin/python
from ttDraw import DrawBase
from OpenGL.GL import *

class DrawArc(DrawBase):
    @property
    def glID(self):
        if self._glID == None:
            self._glID = glGenLists(1)
            glNewList(self._glID,GL_COMPILE)
            glLineWidth(self.size)
            glVerts = self.thing.subdivide(10)
            glBegin(GL_LINE_STRIP)
            for vert in glVerts:
                glVertex3f(*vert)
            glEnd()
            glEndList()
        return self._glID
        
    def draw(self,ds):
        scale = ds.scale
        color = ds.color
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glScalef(scale, scale, scale)
        glColor3f(*color)
        glCallList(self.glID)
        glPopMatrix()

