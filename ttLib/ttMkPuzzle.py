#!/usr/bin/python
from ttCircleFactory import CircleFactory
from ttSphere import Sphere
from ttShell import Shell
from ttPuzzle import Puzzle
from ttSymmetry import Symmetry

class ShellSpec(object):
    def __init__(self,angleList,symmetryList,thickness):
        self.factories = []
        self.thickness = thickness
        for a in angleList:
            for s in symmetryList:
                sc = s.clone()
                self.factories.append(CircleFactory(a,sc))

def puzzleFactory(inrad,shellSpecs):
    insphere = Sphere(inrad)
    prev = insphere
    shellList = []
    for ss in shellSpecs:
        sh = Shell(ss.factories,ss.thickness,prev)
        shellList.append(sh)
        prev = sh
    puz = Puzzle(shellList,insphere)
    return puz

def defaultPuzzle():
    cube = Symmetry(Symmetry.cube)
    specs = [ShellSpec([70],[cube],0.2)]
    puzzle = puzzleFactory(1.0,specs)
    return puzzle

