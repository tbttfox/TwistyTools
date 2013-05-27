#!/usr/bin/python
from DrawBase import DrawBase
from OpenGL.GL import *

class DrawLine(DrawBase):
    def draw(self,ds):
        scale = ds.scale
        color = ds.color
        
        glDisable(GL_LIGHTING)
        glColor3f(*color)
        glLineWidth(self.size)
        glPushMatrix()
        glScale(scale,scale,scale)
        glBegin(GL_LINES)
        glVertex3f(*self.thing.s)
        glVertex3f(*(self.thing.s + self.thing.v))
        glEnd()
        glPopMatrix()

