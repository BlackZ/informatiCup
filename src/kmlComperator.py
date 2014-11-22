# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 16:48:55 2014

@author: adreyer
"""

import Polygon
import kmlData

class KMLComperator():
  
  def __init__(self):
    pass
  
  def compare(self, kml1, kml2):
    if isinstance(kml1,kmlData.KMLObject) and isinstance(kml2,kmlData.KMLObject):
      pass
    else:
      raise TypeError("compare can only compare two kmlObjects")
  
  def _buildPolygon(self, kml):
    poly=Polygon.Polygon()
    for placemark in kml.placemarks:
      coord=[]
      for node in placemark.polygon:
        coord.append((node.lat,node.lon))
      tmppoly=Polygon.Polygon(coord)
      poly=poly|tmppoly
    return poly
  