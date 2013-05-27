#!/usr/bin/python
from ttPoint import Point,cross
from ttCircle import circleIntPlane
from ttLine import Line,lineIntLine
from ttPlane import Plane

#Here, we use a circle with it's point at the origin to represent a cone

def lineIntCone(line,circle):
    #make a 3 point plane using the two points from the line and the apex of the cone
    #get the two lines of intersection with this plane and the cone
    #get the two points of intersection with my ray and the two lines from the previous step
    planeNormal = cross(line.s, line.s+line.v)
    plane = Plane(Point(), planeNormal)
    rays = planeIntCone(plane,circle)
    if rays:
        int1 = lineIntLine(rays[0],line)
        int2 = lineIntLine(rays[1],line)
        return int1,int2
    else:
        return None

def planeIntCone(plane,circle):
    #assumes plane includes the apex
    #2 points = intersect circle with plane
    #return two lines from each point to apex
    points = circleIntPlane(circle,plane)
    if points:
        L1 = Line(points[0], points[0])
        L2 = Line(points[1], points[1])
        return L1, L2
    else:
        return None


