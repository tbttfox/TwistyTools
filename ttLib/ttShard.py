#!/usr/bin/python
from __future__ import division
from ttPoint import Point
from ttSphere import Sphere
from ttBase import TTBase
from ttShardSide import ShardSide,DrawShardSide
from ttRegion import DrawRegion
from ttArc import DrawArc
from ttEnum import ttEnumType
from ttDraw import DrawBase

class Shard(TTBase):
    def __init__(self,region,shell):
        self.enum = ttEnumType.Shard
        self.shell = shell
        self.region = region
        self.inArcs = None

        self._sides = None
        self._children = None
        self._parents = []
        self.setParents()


    @property
    def sides(self):
        if self._sides == None:
            self._sides = []
            for a,pn in zip(self.region.arcs, self.region.posNeg):
                self._sides.append(ShardSide(self,a,pn))
        return self._sides

    @property
    def children(self):
        return [self.region, self.shell]

    def getDrawState(self, drawState):
        ds = drawState.copy()
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material

        inradDs = ds.copy()
        outradDs = ds.copy()
        inradDs.scale = inradDs.scale * self.inrad
        outradDs.scale = outradDs.scale * self.outrad

        states = []
        if self.visible:
            states.append(self.region.getDrawState(inradDs))
            states.append(self.region.getDrawState(outradDs))
            for side in sides
                states.append(side.getDrawState(ds))
        return states

    def cleanup(self):
        self.inArcs = None
        self._parents = None
        self._sides = None
        self.children = []
        self.setChildren()
        self.resetDrawObject()



