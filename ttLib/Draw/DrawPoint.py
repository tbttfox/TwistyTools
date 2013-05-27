#!/usr/bin/python
from DrawBase import DrawBase
from OpenGL.GL import *

class DrawPoint(DrawBase):
    def draw(self,ds):
        scale = ds.scale
        color = ds.color
        glDisable(GL_LIGHTING)
        glBegin(GL_POINTS)
        glColor3f(*color)
        glPointSize(self.size)
        glVertex3f(*(self.thing * scale))
        glEnd()

