# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:09:52 2014

@author: jpoeppel & adreyer
"""

import osmData
#import lxml.etree as ET
import xml.etree.cElementTree as ET

class KML():
  """ Class representing a kml file. Holds a list of contained placemarks.
  """
  
  def __init__(self, placemark=None):
    self.placemarks=[]
    if not placemark==None:
      self.addPlacemark(placemark)
      
  def addPlacemark(self, placemark):
    if not isinstance(placemark, Placemark):
      raise TypeError("addPlacemark only accepts Placemarks.")
    self.placemarks.append(placemark)
    
  def addPlacemarkList(self,placemarkList):
    if not isinstance(placemarkList, list):
      raise TypeError("addPlacemarkList only accepts a list of placemarks.")
    for placemark in placemarkList:
      self.addPlacemark(placemark)
      
  @classmethod
  def parseKML(cls, f):
    tree=ET.parse(f)
    root=tree.getroot()
    nid=1
    res=cls()
    for pm in root.iter("{http://earth.google.com/kml/2.1}Placemark"):
      newPlacemark=Placemark(pm[0].text,None,None,pm[2].text)
      startlat=None
      startlon=None
      for coord in pm.iter("{http://earth.google.com/kml/2.1}coordinates"):
        coordstring = coord.text
        nodes = coordstring.split('\n')
        for node in nodes:
          if node.lstrip()!='':#leaves out the first and last entry because
                               #they don't hold coordinates
            pos = node.split(',')
            lat=pos[0]
            lon=pos[1]
            if startlat==None:
              startlat=lat
              startlon=lon
              newPlacemark.addNode(osmData.Node(nid,lat,lon,{}))
              nid+=1
            elif startlat!=lat or startlon!=lon:
              newPlacemark.addNode(osmData.Node(nid,lat,lon,{}))
              nid+=1
            else:
              startlat=None
              startlon=None
      res.addPlacemark(newPlacemark)
    return res
  
class Placemark():
  
  def __init__(self, name, ruleType, nodeList=None, style="defaultStyle"):
    self.name = name
    self.ruleType = ruleType
    self.style = style
    self.polygon=[]
    if not nodeList==None:
      self.addNodeList(nodeList)
    
  def addNode(self, node):
    if not isinstance(node, osmData.Node):
      raise TypeError("addNode only accepts Nodes.")
    self.polygon.append(node)
  
  def addNodeList(self, nodeList):
    if not isinstance(nodeList, list):
      raise TypeError("addNodeList only accepts a list of nodes.")
    for node in nodeList:
      self.addNode(node)
  
  def hasPolygon(self):
    if len(self.polygon) > 2:
      return True
    else:
      return False
      
  def getXMLTree(self):
    root = ET.Element("Placemark")
    
    name = ET.SubElement(root, "name")
    name.text = self.name
    
    description = ET.SubElement(root, "description")
    description.text ="<img src='"+ self.name + ".jpg' width = '400' />"
    style = ET.SubElement(root, "styleUrl")
    style.text = "#" + self.style
    
    polygon = ET.SubElement(root, "Polygon")
    altitudeMode = ET.SubElement(polygon, "altitudeMode")
    altitudeMode.text = "clampToGround"
    extrude = ET.SubElement(polygon, "extrude")
    extrude.text = str(1)
    tessellate = ET.SubElement(polygon, "tessellate")
    tessellate.text = str(1)
    outerBoundary = ET.SubElement(polygon, "outerBoundaryIs")
    linearRing = ET.SubElement(outerBoundary, "LinearRing")
    
    coordinates = ET.SubElement(linearRing, "coordinates")
    coordinates.text = ""
    for n in self.polygon:
      coordinates.text += n.getCoordinateString()
    
    return root
    
  
