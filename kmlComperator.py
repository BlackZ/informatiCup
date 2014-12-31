# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 16:48:55 2014

@author: adreyer
"""

import Polygon
from isySUR import kmlData
import argparse

class KMLComperator():
  
  def __init__(self):
    pass
  
  def compare(self, kml1, kml2):
    if isinstance(kml1,kmlData.KMLObject) and isinstance(kml2,kmlData.KMLObject):
      poly1=self._buildPolygon(kml1)
      poly2=self._buildPolygon(kml2)
      numberOfPlacemarks1=len(kml1.placemarks)
      numberOfPlacemarks2=len(kml2.placemarks)
      
      overlap=poly1&poly2
      percentage1=overlap.area()/poly1.area()
      percentage2=overlap.area()/poly2.area()
      percentage=(percentage1+percentage2)/2
      
      if numberOfPlacemarks1==numberOfPlacemarks2:
        result=compareResult(numberOfPlacemarks1, percentage)
      else:
        result=compareResult("different", percentage)
        
      return result
    else:
      raise TypeError("compare can only compare two kmlObjects")
  
  def _buildPolygon(self, kml):
    poly=Polygon.Polygon()
    for placemark in kml.placemarks:
      coord=[]
      for node in placemark.polygon:
        pos = node.split(",")
        coord.append((float(pos[0]),float(pos[1])))
      tmppoly=Polygon.Polygon(coord)
      poly=poly|tmppoly
    return poly
    
class compareResult():
  
  def __init__(self, numberOfPlacemarks, percentaceOfOverlap):
    self.numberOfPlacemarks=numberOfPlacemarks
    self.percentaceOfOverlap=percentaceOfOverlap
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='compares the Placemarks of two given .kml-files')
  parser.add_argument('file', nargs=2, type=argparse.FileType('r'), help="valid .kml file")
  args = parser.parse_args()
  Comp = KMLComperator()
  testKML1=kmlData.KMLObject.parseKML(args.file[0])
  testKML2=kmlData.KMLObject.parseKML(args.file[1])
  res = Comp.compare(testKML1,testKML2)
  print "Number of Placemarks in the files: " + str(res.numberOfPlacemarks)
  print "Percentage of Overlap: " + str(res.percentaceOfOverlap*100) + "%"