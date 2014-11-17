# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:09:52 2014

@author: jpoeppel & adreyer
"""

import osmData
import math
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
    
  @property
  def vertices(self):
    """
    This function-property converts the points contained by node objects to a list of tuples
    
    @return listOfPoints: a list of tuples, where each tuple reprent a point (e.g. [(0,0),(0,1),(1,1),(1,0)])
    """
    listOfPoints=[]
    for n in self.polygon:
      listOfPoints.append((n.lat,n.lon))
    return listOfPoints
  
  @property
  def sides(self):
    """
    This function-property returns a list of lists of tuples, which describes all edges of the polygone
    
    @return edgeList: a list of lists of tuples (e.g. [[(0,0),(0,1)],[(0,1),(1,1)]]) a sublist represents an edge 
    """
    edgeList = []
    args = self.vertices
    for i in xrange(-len(args), 0):
      edgeList.append([args[i], args[i + 1]])
    return edgeList
    
  def _distPointLine(self,px,py,x1,y1,x2,y2):
    """
    This function calculates the shortest distance from a point to a line
    
    @param px: x-coord of the point
    @param py: y-coord of the point
    
    @param x1: x-coord of the first point of the line
    @param y1: y-coord of the first point of the line
    @param x2: x-coord of the second point of the line
    @param y2: y-coord of the second point of the line
    
    @return: shortest distance from point to line
    """
    dx = x2 - x1
    dy = y2 - y1
    if dx == dy == 0:  # the segment's just a point
      return math.hypot(px - x1, py - y1)
  
    # Calculate the t that minimizes the distance.
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
  
    # See if this represents one of the segment's
    # end points or a point in the middle.
    if t < 0:
      dx = px - x1
      dy = py - y1
    elif t > 1:
      dx = px - x2
      dy = py - y2
    else:
      near_x = x1 + t * dx
      near_y = y1 + t * dy
      dx = px - near_x
      dy = py - near_y
  
    return math.hypot(dx, dy)
  
  
  def _isPointInsidePolygon(self,x,y):
    """
    This function proves if a points is envolved in a polygone
    
    @param x: x-coord of the point
    @param y: y-coord of the point
    
    @return: true if point is inside
             false if point is outside or on edge
    """
    poly=self.vertices
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
      p2x,p2y = poly[i % n]
      if y > min(p1y,p2y):
        if y <= max(p1y,p2y):
          if x <= max(p1x,p2x):
            if p1y != p2y:
              xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if p1x == p2x or x <= xinters:
              inside = not inside
        p1x,p1y = p2x,p2y

    return inside
    
  def distToPolygon(self, node):
    """
    Function that returns the distance of the given node to the contained polygon.
    
    @param node: The node to which the distance is calculated
    
    @return minDist: The distance to the given node
             if minDist>0 point is outside
             if minDist<0 point is inside
             if mindDist=0 point is on edge
             if the placemark contains no polygon --> #TODO:Errorcode?!? 
    """
    minDist=99999999999
    for s in self.sides:
      dist=self._distPointLine(node.lat,node.lon,s[0][0],s[0][1],s[1][0],s[1][1])
      if dist<minDist:
        minDist=dist
    
    if self._isPointInsidePolygon(node.lat,node.lon):
      minDist=-minDist    
    return minDist
