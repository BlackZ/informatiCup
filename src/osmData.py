# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:31:52 2014
Basic class that holds the osm-data (consisting of basing elements)
@author: adreyer
"""

class OSM():
  
  def __init__(self):
    self.nodes = {}
    self.ways = {}
    self.relations = {}
    
  def addNode(self, node):
    self.nodes[node.id] = node
    
  def addWay(self, way):
    self.ways[way.id] = way
    
  def addRelation(self,relation):
    self.relations[relation.id] = relation


class Node():
  
  def __init__(self, id, lat, lon, tags):
    self.id = id
    self.lat = lat
    self.lon = lon
    self.tags = tags
  
  
class Way():
  
  def __init__(self, id, refs, tags):
    self.id = id
    self.refs = refs
    self.tags = tags
  
  
class Relation():
  
  def __init__(self, id, members, tags):
    self.id = id
    self.members = members
    self.tags = tags