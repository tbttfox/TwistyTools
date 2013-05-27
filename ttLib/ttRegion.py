#!/usr/bin/python
from __future__ import division
from ttPoint import TINYNUM,Point,cross,matMul,angle,distance2,cart2uv
from ttPlane import pointDistPlane
from ttTriangle import Triangle
from ttSphere import Sphere
from ttBase import TTBase

from Draw.DrawRegion import DrawRegion


class Region(TTBase):
    def __init__(self,arcList,pnList):
        """
        Regions are made in the Graph class

        >> Region(arcList,pnList,graph)
        Where:
        arcList is an ordered list of arcs
        pnList is an ordered list of arc "directions" (0 means the arc
            is convex, 1 means the arc is concave)
        baseSide is the list of circles that overlap the current region
        """
        super(Region,self).__init__()
        self.enum = TTBase.enumType.Region

        #these will be reordered
        self.arcs = None
        self.posNeg = None  
        self.corners = None

        self._center = None

        self.allNeg = False
        if sum(pnList) == len(pnList):
            self.allNeg = True

        #here we order the arcs/posNeg/corners

        #if there's only two arcs, everything is already in order
        if len(arcList) > 2:
            arcs = list(arcList[:])
            pn = list(pnList[:])
            if self.allNeg:
                idx = 0
                corn = [arcs[idx].end, arcs[idx].start]
            else: #we have at least one positive arc
                idx = pn.index(0) #grab the first positive arc
                corn = [arcs[idx].start, arcs[idx].end]
            pnOrd = [pn.pop(idx)] #PosNeg Ordered
            arcsOrd = [arcs.pop(idx)] #Arcs Ordered
            #print "arcStart ",arcsOrd[0].start
            #print "arcEnd ",arcsOrd[0].end

            #loop through the list to find if anything begins/ends with the last item on the list
            #while corn[0] != corn[-1]: #go 'till last arc connects to the first
            for _ in range(len(pn)): # looping the variable "_" just means don't use
                found = 0
                for i in range(len(arcs)):
                    if arcs[i].start == corn[-1]:
                        corn.append(arcs[i].end)
                        arcsOrd.append(arcs.pop(i))
                        pnOrd.append(pn.pop(i))
                        found = 1
                        break
                    elif arcs[i].end == corn[-1]:
                        corn.append(arcs[i].start)
                        arcsOrd.append(arcs.pop(i))
                        pnOrd.append(pn.pop(i))
                        found = 1
                        break
                if found == 1:
                    continue
                else:
                    print "problem finding a ccycle in region.__init__"
            self.posNeg = pnOrd
            self.corners = corn[:-1]
            self.arcs = arcsOrd
        self.parents = []
        self.setParents()

    @property
    def center(self):
        if self._center == None:
            if len(self.corners) > 0:
                vecChain = Point(0,0,0)
                for p in self.corners:
                    vecChain = vecChain + p
                #everything is done on the unit sphere
                self._center = vecChain.n
        return self._center
                
    def __eq__(self,other):
        if not isinstance(other,Region): 
            return False
        if len(self.arcs) != len(other.arcs): 
            return False
        for i in range(len(self.arcs)): 
            if self.arcs == other.arcs[i:] + other.arcs[:i]: 
                return True
        return False

    def fanTriangle(self,offset=0):
        corn = self.corners #already sorted 
        if len(corn) < 3: 
            print "Trying to make a triangle out of < 3 corners"
            return None
        corn = corn[offset:] + corn[:offset]
        tris = []
        for i in range(2,len(corn)):
            tris.append(Triangle(corn[0], corn[i-1], corn[i]))
        return tris

    def similar(self,other):
        if not isinstance(other,Region): 
            return False
        if len(self.arcs) != len(other.arcs): 
            return False
        if len(self.arcs) == 2:
            myd = distance2(self.arcs[0].start, self.arcs[0].end)
            yourd = distance2(other.arcs[0].start, other.arcs[0].end)
            if myd != yourd: 
                return False
            myx = distance2(self.arcs[1].c, self.arcs[0].c)
            yourx = distance2(other.arcs[1].c, other.arcs[0].c)
            if myx != yourx: 
                return False
            myrads = sorted([self.arcs[0].rad, self.arcs[1].rad])
            yourrads = sorted([other.arcs[0].rad, other.arcs[1].rad])
            if -TINYNUM < myrads[0] - yourrads[0] < TINYNUM:
                if -TINYNUM < myrads[1] - yourrads[1] < TINYNUM:
                    return True
            return False
        myTris = self.fanTriangle()
        for i in range(len(self.arcs)):
            yourTris = other.fanTriangle(i)
            if myTris == yourTris:
                return True
        return False      

    def contains(self,pt):
        for i,a in enumerate(self.arcs):
            d = pointDistPlane(pt,a.circle.toPlane())
            if self.posNeg[i] == 0 and d < -TINYNUM:
                return False
            elif self.posNeg[i] == 1 and d > TINYNUM:
                return False
        return True


    @property
    def drawObject(self):
        if self._drawObject == None:
            self._drawObject = DrawRegion(self)
        return self._drawObject



def regionCoreRegion(A,B):

    ##TODO##
    # This function relies on a graph object
    # pull this functionality out of the new combined shell object
    # so we can use it here without duplicating code
    ##TODO##

    allCircles = [x.circle for x in A.arcs] + [x.circle for x in B.arcs] 
    allPN = A.posNeg + B.posNeg

    tempGraph = Graph(allCircles)
    keep = []
    ccls = []
    mypn = []

    #for all the arcs in the overlapping regions
    for arc in tempGraph.arcs: 
        mp = arc.midpoint
        if A.contains(mp) and B.contains(mp):
            try:
                idx = allCircles.index(arc.circle)
            except AttributeError:
                continue
            except:
                raise
            keep.append(arc)
            #if the circle is positive in the region
            #it'll be positive in the core
            if allPn[idx] == 0: 
                mypn.append(0)
                ccls.append(arc.circle)
            else:
                mypn.append(1)
    return Region(keep,mypn,tempGraph)
            


