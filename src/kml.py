# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:09:52 2014

@author: jpoeppel & adreyer
"""

import osmData

class KML():
  """ Class representing a kml file. Holds a list of contained placemarks.
  """
  
  
  def __init__(self):
    pass
  
class Placemark():
  
  def __init__(self, name, ruleType, nodeList=None):
    self.name = name
    self.ruleType = ruleType
    if nodeList==None:
      self.polygon = []
    else:      
      self.polygon = nodeList
    
  def addNode(self, node):
    if not isinstance(node, osmData.Node):
      raise TypeError("addNode only accepts Nodes.")
    self.polygon.append(node)
  
  def addNodeList(self, nodeList):
    if not isinstance(nodeList, list):
      raise TypeError("addNodeList only accepts a list of nodes")
    for node in nodeList:
      self.addNode(node)
  
  def hasPolygon(self):
    if len(self.polygon) > 2:
      return True
    else:
      return False
    
  def distToPolygon(self, node):
    """
    Function that returns the distance of the given node to the contained polygon.
    
    @param node: The node to which the distance is calculated
    
    @return: The distance to the given node, if the placemark contains a polygon, else error code #TODO which code!!!
    """
    pass