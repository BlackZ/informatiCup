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
    if isinstance(node,Node):
      self.nodes[node.id] = node
    else:
      raise TypeError("addNode only accepts nodes.")
      
      
  def addNodeList(self, nodeList):
    for node in nodeList:
      self.addNode(node)
    
  def addWay(self, way):
    if isinstance(way,Way):
      self.ways[way.id] = way
    else:
      raise TypeError("addWay only accepts ways.")
    
  def addRelation(self,relation):
    if isinstance(relation,Relation):
      self.relations[relation.id] = relation
    else:
      raise TypeError("addRelation only accepts relations.")
      
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

    Parameters
    ==========
    
    @param identifier: The id of the node.
    
    @type identifier: Will be parsed to string
    
    @param lat: Latitude of the node as float.
    
    @type lat: Will be parsed to float.
    
    @param lon: Longitude of the node as float.
    
    @type lon: Will be parsed to float.
    
    @param tags: A dictionary containing all the tags for the node.
    """
    self.id = str(identifier)
    self.lat = float(lat)
    self.lon = float(lon)
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary.")
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
    """
    Basic class containing an osm Way
    
    @param identifier: The id of the way as a string
    
    @param refs: An ordered list of node id's (strings) that make up the way
    
    @param tags: A dictionary containing all the tags for the way
    """
    self.id = str(identifier)
    if not isinstance(refs, list):
      raise TypeError("refs must be a list of id's")
    self.refs = [str(r) for r in refs]
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary")
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
    """
    Basic class containing an osm Relation
    
    @param identifier: The id of the way as a string
    
    @param members: A list of tripel (membertype[e.g.  way], id of the member, addition tags [e.g. outer])
    
    @param tags: A dictionary containing all the tags for the way
    """
    self.id = str(identifier)
    if not isinstance(members, list):
      raise TypeError("members need to be a list of tripel")
    self.members = [tuple(m) for m in members]   
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary")
    self.tags = tags
   
  def __eq__(self,other):   
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.members == other.members 
      and self.tags == other.tags)
   
  def __ne__(self,other):
    return not self.__eq__(other)