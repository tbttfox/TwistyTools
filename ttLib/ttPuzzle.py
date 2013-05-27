#!/usr/bin/python
from ttBase import TTBase,DrawState
from ttPoint import distance


class Puzzle(TTBase):
    def __init__(self,shellList,insphere):
        super(Puzzle,self).__init__()
        self.enum = self.enumType.Puzzle
        self.label = "Puzzle"
        self.shellList = shellList
        self.insphere = insphere
        self._children = None
        self._parents = None
        self._pieces = None
        self.setParents()

    def copyShell(self, index):
        newShell = self.shellList[index].clone()
        newShell.parents = []
        self.shellList.insert(index+1, newShell)
        newShell.innerObject = self.shellList[index]
        if newShell is not self.shellList[-1]:
            self.shellList[index+2].innerObject = newShell

        self.setParents()
        for sh in self.shellList:
            sh.cleanup()
        self.cleanup()

    def deleteShell(self,index):
        if len(self.shellList) == 1:
            #raise Can't Delete Last Shell error
            return
        if index == 0: #removing the first one
            self.shellList[1].innerObject = self.insphere
        elif index < len(self.shellList) - 1: #not removing the last one
            self.shellList[index+1].innerObject = self.shellList[index-1]
        del self.shellList[index]
        for sh in self.shellList:
            sh.cleanup()
        self.cleanup()

    @property
    def children(self):
        return [self.insphere] + self.shellList  

    def cleanup(self):
        self._children = None
        self._parents = None
        self.dirtyPieces()
        self.setParents()

    def dirtyPieces(self,*args,**kwargs):
        self._pieces = None


    def getDrawState(self):
        ds = DrawState()
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material
        state = self.insphere.getDrawState(ds)
        for sh in self.shellList:
            state.extend(sh.getDrawState(ds))
        return state

    def rayPick(self,ray):
        """
        YAY Picking!!
        so this guy's gonna dig through the hierarchy
        and return a list of tuples with (normalizedDistance, object)
        """
        hits = []
        inhit = self.insphere.rayPick(ray)
        if inhit:
            hits.extend(inhit)
        for sh in self.shellList:
            shit = sh.rayPick(ray)
            if shit: #tee hee
                hits.extend(shit)

        #get the far point and raylength
        farpoint = ray.s + ray.v
        raylength = abs(ray.v)

        #get the hit distances from the far point, paired with the hit objs
        dhit = [(distance(pt,farpoint),item) for pt,item in hits]
        dhit = [(raylength - dst,item) for dst,item in dhit if dst < raylength]
        dhit.sort()
        if dhit:
            dsts,objs = zip(*dhit)
            return objs
        else:
            return []

    @property
    def pieces(self):
        if self._pieces is None:
            self.autoPieces()
        return self._pieces

    def autoPieces(self):
        ''' Do a first-pass at combining shards into pieces '''
        #############################################################################
        #this function will only ever be needed in this scope, 
        #so define it in this scope, and Yay recursion!
        def drillPieces(regionGroups, shellList, connections, pieceNum, shell, group, index):
            nShell = shell + 1
            if nShell < len(regionGroups):
                for nGroup in range(len(regionGroups[nShell])):
                    if len(regionGroups[shell][group]) != len(regionGroups[nShell][nGroup]):
                        continue
                    for nIndex in range(len(regionGroups[nShell][nGroup])):
                        if regionSimCircleRegion(regionGroups[shell][group][index], shellList[shell],
                                    regionGroups[nShell][nGroup][nIndex], shellList[nShell]):
                            connections[nShell][nGroup][nIndex] = pieceNum
                            dpr = drillPieces(regionGroups,shellList,connections,pieceNum,nShell,nGroup,nIndex)
                            dpr.append(regionGroups[shell][group][index])
                            return dpr
            return [regionGroups[shell][group][index]]
        #############################################################################

        if len(self.shellList) == 0:
            self._pieces = [] #return Nothing
            return
        elif len(self.shellList) == 1:
            sortie = self.shellList[0].regionSort
            self._pieces = [[i[0]] for i in sortie] #return unique regions
            return

        #get shards as [shell[group[piece]]]
        regionGroups = [sl.regionSort for sl in self.shellList]
        connections = [[[None for shd in grp ] for grp in sh ] for sh in regionGroups]

        pieceCounter = 0
        pieceList = []
        for shn,shl in enumerate(regionGroups):
            for gpn,grp in enumerate(shl):
                if connections[shn][gpn].count(None) == len(connections[shn][gpn]):
                    pieceList.append(drillPieces(regionGroups,self.shellList,connections,pieceCounter,shn,gpn,0))
                    pieceCounter += 1
        #self._pieces = [Piece(a) for a in pieceList]
        self._pieces = pieceList


#TODO  Move this back to ttRegion.py
def regionSimCircleRegion(r1,sh1,r2,sh2):
    if len(r1.arcs) != len(r2.arcs):
        return False

    #get lists of the circles in the arcs
    s1cList = [r1a.circle for r1a in r1.arcs]
    s2cList = [r2a.circle for r2a in r2.arcs]

    s1nLargestList = [sh1.getNLargest(ccl) for ccl in s1cList]
    s2nLargestList = [sh2.getNLargest(ccl) for ccl in s2cList]

    #in all possible list rotation offsets
    for offset in range(len(s1cList)):
        #shard2 Offset Largest List
        s2oll = s2nLargestList[offset:] + s2nLargestList[:offset]
        if s2oll == s1nLargestList:
            #shard2 offset circle list
            s2ocl = s2cList[offset:] + s2cList[:offset]

            #the only thing that's gonna be equal about the
            #circles in these lists are the axes
            norms1 = [c.n for c in s2ocl]
            norms2 = [c.n for c in s1cList]
            if norms1 == norms2:
                return True
    return False





