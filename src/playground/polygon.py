# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:52:11 2014

@author: adreyer
"""

import Polygon#, Polygon.IO

p1=Polygon.Polygon(((0.0,4.0),(6.0,3.0),(9.0,6.0),(8.0,10.0)))

p2=Polygon.Polygon(((3.0,3.0),(9.0,0.0),(12.0,4.0),(10.0,9.0)))

p3=p1&p2

print(p1.area())
print(p2.area())
print(p3.area())

#Polygon.IO.writeSVG('p1.svg',(p1,p2,p3))