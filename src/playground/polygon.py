# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:52:11 2014

@author: adreyer
"""

#import Polygon#, Polygon.IO
from sympy import *
from sympy.geometry import *

#p1, p2, p3, p4, p5 = [(0, 0), (1, 0), (5, 1), (0, 1), (3, 0)]
p1, p2, p3, p4 = [(0, 0), (0, 1), (1, 1), (1, 0)]
testPoly=Polygon(p1, p2, p3, p4)
testPoint=Point(0.5,2.5)
testPoint2=Point(0.5,0.5)
testPoint3=Point(0,0.5)
testPoint4=Point(0,0)
print "============================"
print "Punkt außerhalb"
print "----------------------------"
print "Abstand: " + str(testPoly.distance(testPoint))
print "Enthalten: " + str(testPoly.encloses_point(testPoint))
print "============================"
print "Punkt innerhalb"
print "----------------------------"
print "Abstand: " + str(testPoly.distance(testPoint2))
print "Enthalten: " + str(testPoly.encloses_point(testPoint2))
print "============================"
print "Punkt auf Rand"
print "----------------------------"
print "Abstand: " + str(testPoly.distance(testPoint3))
print "Enthalten: " + str(testPoly.encloses_point(testPoint3))
print "============================"
print "Punkt in einer Ecke"
print "----------------------------"
print "Abstand: " + str(testPoly.distance(testPoint4))
print "Enthalten: " + str(testPoly.encloses_point(testPoint4))


#p1=Polygon.Polygon(((0.0,4.0),(6.0,3.0),(9.0,6.0),(8.0,10.0)))

#p2=Polygon.Polygon(((3.0,3.0),(9.0,0.0),(12.0,4.0),(10.0,9.0)))

#p3=p1&p2

#test, if point is inside a polygon
#this function cant test, whether the point is in the border or not
#print "Inside: ", p1.isInside(5.0, 6.0)
#print "On Border: ", p1.isInside(0.0, 4.0)
#print "On Border: ", p1.isInside(6.0, 3.0)
#print "Outside: ", p1.isInside(0.0, 2.0)

#print(p1.area())
#print(p2.area())
#print(p3.area())

#Polygon.IO.writeSVG('p1.svg',(p1,p2,p3))