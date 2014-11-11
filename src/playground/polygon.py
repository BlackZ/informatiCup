# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:52:11 2014

@author: adreyer
"""

import Polygon#, Polygon.IO

p1=Polygon.Polygon(((0.0,4.0),(6.0,3.0),(9.0,6.0),(8.0,10.0)))

p2=Polygon.Polygon(((3.0,3.0),(9.0,0.0),(12.0,4.0),(10.0,9.0)))

p3=p1&p2

#test, if point is inside a polygon
#this function cant test, whether the point is in the border or not
print "Inside: ", p1.isInside(5.0, 6.0)
print "On Border: ", p1.isInside(0.0, 4.0)
print "On Border: ", p1.isInside(6.0, 3.0)
print "Outside: ", p1.isInside(0.0, 2.0)

print(p1.area())
print(p2.area())
print(p3.area())

#Polygon.IO.writeSVG('p1.svg',(p1,p2,p3))