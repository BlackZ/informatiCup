# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:31:52 2014
Basic class that holds the osm-data (consisting of basing elements)
@author: adreyer
"""

import sys

class OSM():
  
  def __init__(self):
    self.nodes = {}
    self.ways = {}
    self.relations = {}
    
  def addNode(self, node):
    if isinstance(node,Node):
      self.nodes[node.id] = node
    else:
      print "Error: addNode only accepts nodes."
      sys.exit(-1)
    
  def addWay(self, way):
    if isinstance(way,Way):
      self.ways[way.id] = way
    else:
      print "Error: addWay only accepts ways."
      sys.exit(-1)
    
  def addRelation(self,relation):
    if isinstance(relation,Relation):
      self.relations[relation.id] = relation
    else:
      print "Error: addRelation only accepts relations."
      sys.exit(-1)

class Node():
  
  def __init__(self, identifier, lat, lon, tags):
    self.id = identifier
    self.lat = lat
    self.lon = lon
    self.tags = tags
  
  
class Way():
  
  def __init__(self, identifier, refs, tags):
    self.id = identifier
    self.refs = refs
    self.tags = tags
  
  
class Relation():
  
  def __init__(self, identifier, members, tags):
    self.id = identifier
    self.members = members
    self.tags = tags