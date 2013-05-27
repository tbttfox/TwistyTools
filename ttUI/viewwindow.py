#!/usr/bin/env python
from __future__ import division

from ttLib.ttLine import Line
from ttLib.ttPoint import Point
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class ViewWindow(QtOpenGL.QGLWidget):
    class Modes:
        manip = 1
        pick = 0

    def __init__(self, parent=None):
        super(ViewWindow,self).__init__(parent)
        self.rot = [30,45,0]
        self.tran = [0,0,0]
        self.zoom = [0,0,-10]
        self.mode = self.Modes.pick
        self.lastPos = QtCore.QPoint()
        self.ray = None
        self.puzzle = None

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def initializeGL(self):
        glClearColor(.5,.5,.5,0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_AUTO_NORMAL) #calculates normals for NURBS
        glEnable(GL_NORMALIZE) #automatically normalizes surfaceNormals
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE,1)
        glEnable(GL_COLOR_MATERIAL)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(*self.zoom)
        glTranslated(*self.tran)
        glRotated(self.rot[0], 1, 0, 0)
        glRotated(self.rot[1], 0, 1, 0)
        glRotated(self.rot[2], 0, 0, 1)
        self.puzzle.draw()
        #if self.ray:
            #self.ray.draw(1)

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, width/height, .01, 20)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.mod =  QtGui.QApplication.keyboardModifiers()
        self.lastPos = QtCore.QPoint(event.pos())
        if self.mod & Qt.AltModifier:
            self.mode = self.Modes.manip
        else:
            self.ray = self.clickRay(event.x(), event.y())
            self.pick()

    def pick(self):
        self.puzzle.rayPick(self.ray)

    def registerPuzzle(self,puzzle):
        self.puzzle = puzzle
        self.puzzle.setScene(self)
        self.puzzle.revealAll()

    def mouseMoveEvent(self, event):
        if self.mode == self.Modes.manip:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()
            if event.buttons() & QtCore.Qt.LeftButton:
                self.rot[0]= self.rot[0] + dy/2
                self.rot[1]= self.rot[1] + dx/2
            elif event.buttons() & QtCore.Qt.MidButton:
                self.tran[0]= self.tran[0] + dx/100
                self.tran[1]= self.tran[1] - dy/100 
            elif event.buttons() & QtCore.Qt.RightButton:
                self.zoom[2]= self.zoom[2] + dy/100
            self.lastPos = QtCore.QPoint(event.pos())
            self.updateGL()

    def mouseReleaseEvent(self,event):
        self.mode = self.Modes.pick

    def clickRay(self, mouseX, mouseY):
        """ I found out how to do this online from nehe   """
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        mouseY = viewport[3] - mouseY 
        near = gluUnProject(mouseX, mouseY, 0, modelview, projection, viewport)
        far = gluUnProject(mouseX, mouseY, 1, modelview, projection, viewport)
        near = Point(*near)
        far = Point(*far)
        return Line(near, far-near)


