#!/usr/bin/python
from __future__ import division
from DrawBase import DrawBase
from ttLib.ttSymmetry import Symmetry
from OpenGL.GL import *

class DrawSphere(DrawBase):
    @property
    def glID(self):
        if self._glID == None:
            #recursive drawing function
            def nxt(a,b,c,height):
                if height <= 0: #endCase
                    #draw the triangle with the correct normals
                    glNormal3f(*a)
                    glVertex3f(*a)
                    glNormal3f(*b)
                    glVertex3f(*b)
                    glNormal3f(*c)
                    glVertex3f(*c)
                else:
                    #normalize the midpoints
                    ab = ((a + b) / 2).n
                    ac = ((a + c) / 2).n
                    bc = ((c + b) / 2).n
                    #make 4 triangles out of the points
                    nxt(a,ab,ac,height-1)
                    nxt(b,bc,ab,height-1)
                    nxt(c,ac,bc,height-1)
                    nxt(ab,bc,ac,height-1)

            self._glID = glGenLists(1)
            sym = Symmetry(Symmetry.dodecahedron)
            glNewList(self._glID,GL_COMPILE)
            glBegin(GL_TRIANGLES)
            triangles = [[0,1,5],  [0,2,1],  [0,3,2],  [0,4,3],  [0,5,4],
                        [11,9,10], [11,8,9], [11,7,8], [11,6,7], [11,10,6],
                        [5,1,6],   [1,2,7],  [2,3,8],  [3,4,9],  [4,5,10],
                        [10,9,4],  [9,8,3],  [8,7,2],  [7,6,1],  [6,10,5]]
            for t in triangles:
                nxt(sym[t[0]],sym[t[1]],sym[t[2]],3)
            glEnd()
            glEndList()
        return self._glID

    def draw(self,ds):
        scale = ds.scale
        material = ds.material
        glEnable(GL_LIGHTING)
        glPushMatrix()
        glColor3f(*material)
        glScale(scale,scale,scale)
        glCallList(self.glID)
        glPopMatrix()


