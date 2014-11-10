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
      
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    
    return (self.nodes == other.nodes 
      and self.ways == other.ways
      and self.relations == other.relations)

  def __ne__(self,other):
    return not self.__eq__(other)
    
    

class Node():
  
  def __init__(self, identifier, lat, lon, tags):
    self.id = identifier
    self.lat = lat
    self.lon = lon
    self.tags = tags
    
  def __eq__(self,other):
    if not isinstance(other,self.__class__):
      return False
    
    return (self.id == other.id 
      and self.lat == other.lat 
      and self.lon == other.lon
      and self.tags == other.tags)
      
  def __ne__(self,other):
    return not self.__eq__(other)
  
  
class Way():
  
  def __init__(self, identifier, refs, tags):
    self.id = identifier
    self.refs = refs #Ordered list of node id's that make up the way
    self.tags = tags
    
  def __eq__(self,other):
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.refs == other.refs 
      and self.tags == other.tags)
      
  def __ne__(self,other):
    return not self.__eq__(other)
  
  
class Relation():
  
  def __init__(self, identifier, members, tags):
    self.id = identifier
    self.members = members #List of tripel (membertype[eg way], id of the member, addition tags [eg outer] )
    self.tags = tags
   
  def __eq__(self,other):   
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.members == other.members 
      and self.tags == other.tags)
   
  def __ne__(self,other):
    return not self.__eq__(other)