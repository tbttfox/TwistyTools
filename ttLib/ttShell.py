#!/usr/bin/python
from ttBase import TTBase
from copy import copy
from ttCircle import circleIntCircle
from ttSphere import Sphere
from ttValue import Value
from ttPlane import pointDistPlane
from ttPoint import TINYNUM
from ttArc import Arc,pointsCutCircle
from ttRegion import Region
from Draw.DrawSphere import DrawSphere



class Shell(TTBase):
    def __init__(self,factoryList,thickness,innerObject):
        super(Shell,self).__init__()

        #graph properties
        self.factoryList = factoryList
        self._circles = None
        self._children = None
        self._arcs = None
        self._regions = None
        self.insides = None
        self.outsides = None

        #shell properties
        self._thickness = Value(thickness,"Thickness")
        self.innerObject = innerObject
        self._regionSort = None
        self.nLargest = []
        self.unitSphere = Sphere()

        #base properties
        self.label = "Shell"
        self.enum = TTBase.enumType.Shell
        self._children = None
        self.setParents()

    #graph properties
    def copyLastFactory(self):
        newFactory = self.factoryList[-1].clone()
        newFactory.parents = []
        self.setParents()
        self.factoryList.append(newFactory)
        self.cleanup()

    def deleteFactory(self,index):
        del self.factoryList[index]
        self.cleanup()

    @property
    def circles(self):
        if self._circles == None:
            self._circles = []
            for f in self.factoryList:
                self._circles.extend(f.circles)
        return self._circles

    def getNLargest(self,circle):
        ''' This can be majorly optimized ... shouldn't be too bad though'''
        factorySort = sorted(self.factoryList, key=lambda x: x.angle.value)
        for i,fact in enumerate(factorySort):
            if circle in fact.circles:
                return i

    #Region-builder stuff
    @property
    def arcs(self):
        if self._arcs == None:
            uniqueCircles = list(set(self.circles))
            self._arcs = cutCircleList(uniqueCircles)
        return self._arcs    

    @property
    def regions(self):
        """
        There is a Region on each side of an Arc
        Each Region overlaps a **usually unique list of circles
        self.insides is the list of Circles overlapping
            the Region on the inside of the Arc
        self.outsides is the list of Circles overlapping
            the Region on the outside of the Arc
        To make a region,  we make the lists of overlapping
            Circles and comchilde 
        When we find lists that are equal, that means those
            Arcs are borders of the same Region

        If a Point is on the positive side of a Plane
            then that Point must be contained within the circle
            if both the Circle and Point are on the same Sphere

        ** things like adjascent X-centers on a gigaminx have
           non-unique overlaps. They ARE, however, disjoint
           We will check for disjoint cycles when 
           we combine arcs into regions.
        """
        if self._regions == None:
            self.insides = {}
            self.outsides = {}
            for a in self.arcs:
                self.insides[a] = []
                self.outsides[a] = []
                mp = a.midpoint
                for c in self.circles:
                    d = pointDistPlane(mp,c.toPlane())
                    if -TINYNUM < d < TINYNUM:
                        #the arc is childt of the current circle
                        #that means that only the inside region
                        #overlaps the current circle
                        self.insides[a].append(c)
                    elif d > 0:
                        #the arc is somewhere inside the circle
                        #so both the inside and outside regions
                        #overlap the current circle
                        self.insides[a].append(c)
                        self.outsides[a].append(c)

            #Now that we have the sides,  make a frozenset of each circleList
            #this makes it possible create a dictionary keyed from the circleLists
            setList = []
            for a in self.arcs:
                inset = frozenset(self.insides[a])
                outset = frozenset(self.outsides[a])
                setList.append(inset)
                setList.append(outset)
                self.insides[a] = inset
                self.outsides[a] = outset
            setList = list(set(setList)) #there will be this many regions
           
            bucketDict = {}
            bucketDict = dict([(sl, []) for sl in setList])
            for a in self.arcs:
                #construct lists of (arc,posNeg)
                bucketDict[self.insides[a]].append((a,0))
                bucketDict[self.outsides[a]].append((a,1))

            self._regions = []
            zippedLists = bucketDict.values() #pull those lists
            for z in zippedLists:
                arcList,pnList = zip(*z) #unzips a list
                self._regions.append(Region(arcList,pnList))
        return self._regions

    #shell properties
    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self,value):
        self._thickness.value = value

    @property
    def inrad(self):
        return self.innerObject.outrad

    @property
    def outrad(self):
        return self.inrad + self.thickness.value


    @property
    def regionSort(self):
        '''
        Here we take the regions in a shell and separate them by type
        The number of similar regions in a group must match when
        connecting regions between shells to make pieces
        '''
        if self._regionSort == None:
            sims = []
            for reg in self.regions:
                found = False
                for i in range(len(sims)):
                    if reg.similar(sims[i][0]):
                        sims[i].append(reg)
                        found = True
                        continue
                if not found:
                    sims.append([reg])
            self._regionSort = sims
        return self._regionSort

    #object properties
    @property
    def children(self):
        return [self.thickness] + self.factoryList

    def cleanup(self):
        self._circles = None
        self._children = None
        self._arcs = None
        self._regions = None
        self._regionSort = None
        self._drawCuts = None
        self.setParents()

    def getDrawState(self, drawState):
        ds = drawState.copy()
        ds.inrad = self.inrad
        ds.outrad = self.outrad
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material
        
        inradDs = ds.copy()
        outradDs = ds.copy()
        inradDs.scale = inradDs.scale * self.inrad
        outradDs.scale = outradDs.scale * self.outrad

        states = []
        for f in self.factoryList:
            states.extend(f.getDrawState(inradDs))
            states.extend(f.getDrawState(outradDs))
            if not self.visible:
                states.extend(f.getCutsDrawState(ds))
        if self.visible:
            states.extend(self.unitSphere.getDrawState(outradDs))


        #don't do this yet ... draw regions/shards if they're called for
        if False:
            for reg in self.regions:
                states.extend(reg.getDrawState(ds))

        return states
            
    def pickRegion(self,hits):
        '''
        for the first two hits, 
        check to see what region they're in
        use pointInRegion (or whatever I've called it)

        the rest of the hits are on the cones
        check the circles to see which ones it hits
        '''
        return []

    def rayPick(self,ray):
        hits = []

        outsphere = Sphere(self.outrad)
        hits.extend(outsphere.rayPick(ray))

        for cf in self.factoryList:
            hits.extend(cf.rayPick(ray,self.inrad,self.outrad))

        pickRegions = False #for now
        if pickRegions:
            hits.extend(self.pickRegion(hits))

        return hits

    def clone(self):
        flist = [f.clone() for f in self.factoryList]
        return Shell(flist, self.thickness.value, self.innerObject)




def cutCircleList(circles):
    cornerList = []
    arcList = []
    #intersect all circles with all other circles
    for i in range(len(circles)-1):
        for j in range(i+1,len(circles)):
            cl = circleIntCircle(circles[i],circles[j])
            if cl != None:
                cornerList.append(cl[0])
                cornerList.append(cl[1])
    for c in circles:
        alist = pointsCutCircle(cornerList,c)
        if alist != None:
            arcList.extend(alist)
    return arcList


