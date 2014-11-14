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
      
      
  def addNodeList(self, nodeList):
    for node in nodeList:
      self.addNode(node)
    
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
    """
    Basic class containing an osm Node

    @param identifier: The id of the node as a string.
    
    @param lat: Latitude of the node as float
    
    @param lon: Longitude of the node as float
  
    @param tags: A dictionary containing all the tags for the node
    """
    self.id = str(identifier)
    self.lat = float(lat)
    self.lon = float(lon)
    self.tags = dict(tags)
    
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
    """
    Basic class containing an osm Way
    
    @param identifier: The id of the way as a string
    
    @param refs: An ordered list of node id's (strings) that make up the way
    
    @param tags: A dictionary containing all the tags for the way
    """
    self.id = str(identifier)
    if not isinstance(refs, list):
      raise TypeError
    self.refs = [str(r) for r in refs]
    self.tags = dict(tags)
    
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
    """
    Basic class containing an osm Relation
    
    @param identifier: The id of the way as a string
    
    @param members: A list of tripel (membertype[e.g.  way], id of the member, addition tags [e.g. outer])
    
    @param tags: A dictionary containing all the tags for the way
    """
    self.id = str(identifier)
    if not isinstance(members, list):
      raise TypeError
    self.members = [tuple(m) for m in members]    
    self.tags = dict(tags)
   
  def __eq__(self,other):   
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.members == other.members 
      and self.tags == other.tags)
   
  def __ne__(self,other):
    return not self.__eq__(other)