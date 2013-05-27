#! /usr/bin/python
from ttPoint import Point
from ttBase import TTBase

class Symmetry(TTBase):
    enum = TTBase.enumType.Symmetry

    custom = -1
    tetrahedron = 0
    octahedron = 1
    cube = 2
    rhDodeca = 3
    dodecahedron = 4
    icosahedron = 5
    rhTriacontahedron = 6

    typeList = ["Tetrahedron", "Octahedron", "Cube", "Rhombic Dodecahedron", "Dodecahedron", "Icosahedron", "Rhombic Triacontahedron"]


    def __repr__(self):
        return "<ttLib.ttSymmetry.Symmetry " + self.value +  " object>"

    @property
    def value(self):
        if self.index < 0:
            return "Custom"
        elif self.index >= len(self.typeList):
            return "NONE"
        else:
            return self.typeList[self.index]

    def __getitem__(self,index):
        return self.symmetry[index]

    def __iter__(self):
        for i in self.symmetry:
            yield i

    def __init__(self,index,customList=None):
        super(Symmetry,self).__init__()
        self.label = "Symmetry"
        phi = (5.0**0.5 + 1.0) / 2.0
        tet = [(1,1,1), (1,-1,-1), (-1,-1,1), (-1,1,-1)]
        och = [(1,-1,1), (-1,-1,1), (-1,1,1), (1,1,1), (1,-1,-1), (-1,-1,-1), (-1,1,-1), (1,1,-1)]
        cube = [(0,0,1), (0,-1,0), (-1,0,0), (0,1,0), (1,0,0), (0,0,-1)]
        rhd = [(0,1,1), (1,0,1), (0,-1,1), (-1,0,1), (-1,1,0), (1,1,0),
                (1,-1,0), (-1,-1,0), (-1,0,-1), (0,1,-1), (1,0,-1), (0,-1,-1)]
        dod = [(phi-1,0,1), (1,1-phi,0), (0,-1,phi-1), (1-phi,0,1), (0,1,phi-1), (1,phi-1,0),
                (phi-1,0,-1), (0,-1,1-phi), (-1,1-phi,0), (-1,phi-1,0), (0,1,1-phi), (1-phi,0,-1)]
        ico = [(1,1+phi,0), (phi,phi,-phi), (phi,phi,phi), (-1,1+phi,0), (-phi,phi,-phi),
                (0,1,-1-phi), (1+phi,0,-1), (1+phi,0,1), (0,1,1+phi), (-phi,phi,phi),
                (-1-phi,0,1), (-1-phi,0,-1), (0,-1,-1-phi), (phi,-phi,-phi), (phi,-phi,phi),
                (0,-1,1+phi), (-phi,-phi,phi), (-phi,-phi,-phi), (1,-1-phi,0), (-1,-1-phi,0)]
        rht = [(0,2,0), (1,phi,phi-1), (-1,phi,phi-1), (-1,phi,1-phi), (1,phi,1-phi),
                (phi-1,1,-phi), (1-phi,1,-phi), (1-phi,1,phi), (phi-1,1,phi), (phi,phi-1,1),
                (phi,phi-1,-1), (-phi,phi-1,-1), (-phi,phi-1,1), (-2,0,0), (0,0,-2),
                (2,0,0), (0,0,2), (phi,1-phi,1), (phi,1-phi,-1), (-phi,1-phi,-1),
                (-phi,1-phi,1), (1-phi,-1,phi), (phi-1,-1,phi), (phi-1,-1,-phi), (1-phi,-1,-phi),
                (-1,-phi,1-phi), (-1,-phi,phi-1), (1,-phi,phi-1), (1,-phi,1-phi), (0,-2,0)]

        tetrahedron = [Point(*i).n for i in tet]
        octahedron = [Point(*i).n for i in och]
        cube = [Point(*i).n for i in cube]
        rhDodeca = [Point(*i).n for i in rhd]
        dodecahedron = [Point(*i).n for i in dod]
        icosahedron = [Point(*i).n for i in ico]
        rhTriacontahedron = [Point(*i).n for i in rht]

        self.symList = [tetrahedron, octahedron, cube, rhDodeca, dodecahedron, icosahedron, rhTriacontahedron]
        self.customList = customList
        self._index = index
        if self._index == self.custom:
            self.customList = [Point(*x).n for x in self.customList]
            self.symmetry = self.customList
        else:
            self.symmetry = self.symList[self._index]
        self.setParents()

    @property
    def index(self):
        return self._index
            
    @index.setter
    def index(self,index):
        self._index = index
        self.symmetry = self.symList[self._index]


    def getDrawState(self, drawState):
        ds = drawState.copy()
        if self.color:
            ds.color = self.color
        if self.material:
            ds.material = self.material
        states = []
        if self.visible:
            for p in self.symmetry:
                states.extend(p.getDrawState(ds))
        return states

    def clone(self):
        return Symmetry(self.index)

