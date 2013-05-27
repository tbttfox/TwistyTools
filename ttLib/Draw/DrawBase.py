#!/usr/bin/python
from OpenGL.GL import glDeleteLists

class DrawBase(object):
    def __init__(self,thing,size=3,color=(0,1,0)):
        self.thing = thing
        self.size = size #for line/point thickness
        self.color = color
        self._glID = None
        self._glVerts = None
        self._drawList = None

    def __del__(self):
        if self._glID:
            glDeleteLists(self._glID,1)

