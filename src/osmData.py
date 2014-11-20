# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:31:52 2014
Basic class that holds the osm-data (consisting of basing elements)
@author: adreyer
"""
import sys
import math

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
  
  def getNearestPoly(self,node):
    """
    This function returns the id of the polygon(way) which is closest to the given node
    
    @param node: node for which the function have to compute closest polygon
    @type node: osmData.Node
    
    @return Tupel(id,distance)
    """
    #nearestPoly=(None,-4)
    #for way in self.ways:
    #  if way.hasPolygon(): 
    #    vertices=self._vertices(way.refs)
    #    dist=Way.distToPolygon(node,poly)
    #    if nearestPoly[1]>dist:
    #      nearestPoly=(way.id,dist)
    #return nearestPoly
    pass
  
  def getNearestNode(self,):
    pass
  
  def getNearestRelation(self,):
    pass
  
    
  def _vertices(self,nodeList):
    """
    This function converts the points contained by node objects to a list of tuples
    
    @return listOfPoints: a list of tuples, where each tuple reprent a point (e.g. [(0,0),(0,1),(1,1),(1,0)])
    """
    listOfPoints=[]
    for n in nodeList:
      listOfPoints.append(self.nodes[n].coords)
    return listOfPoints
  

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
    
  def getCoordinateString(self):
    return str(self.lon) + "," +str(self.lat)
    
  def __eq__(self,other):
    if not isinstance(other,self.__class__):
      return False
    
    return (self.id == other.id 
      and self.lat == other.lat 
      and self.lon == other.lon
      and self.tags == other.tags)
      
  def __ne__(self,other):
    return not self.__eq__(other)
  
  @property
  def coords(self):
    """
    This function-property returns latitude and longitude as tupel
    
    @return (lat,lon) as tupel
    """
    return (self.lat,self.lon)
  
  def distToNode(self,node):
    """
    This function computes the distance between two points
    
    @param node: the node the distance should be computed with
    @type node: osmData.Node
    
    @return distance between both nodes
    """
    if not isinstance(node, Node):
      raise TypeError("distToNode only accepts Nodes from type osmData.Node")
    return math.hypot(node.lat - self.lat, node.lon - self.lon)
  
  
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
  
  def hasPolygon(self):
    """
    This functions prooves if the Way has a polygon
    
    @return true if polygon exists
    """
    if len(self.refs)>=4 and self.refs[0]==self.refs[-1]:
      return True
    return False
  
  def __eq__(self,other):
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.refs == other.refs 
      and self.tags == other.tags)
      
  def __ne__(self,other):
    return not self.__eq__(other)
  
  def _sides(self,vertices):
    """
    This function returns a list of lists of tuples, which describes all edges of the polygone
    
    @return edgeList: a list of lists of tuples (e.g. [[(0,0),(0,1)],[(0,1),(1,1)]]) a sublist represents an edge 
    """
    edgeList = []
    args = vertices
    for i in xrange(-len(args), -1):
      edgeList.append([args[i], args[i + 1]])
    return edgeList
  
  def _distPointLine(self,px,py,x1,y1,x2,y2):
    """
    This function calculates the shortest distance from a point to a line
    
    @param px: x-coord of the point
    @type px: float
    @param py: y-coord of the point
    @type py: float
    
    @param x1: x-coord of the first point of the line
    @type x1: float
    @param y1: y-coord of the first point of the line
    @type y1: float
    @param x2: x-coord of the second point of the line
    @type x2: float
    @param y2: y-coord of the second point of the line
    @type y1: float
    
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
  
  def _isPointInsidePolygon(self, coords,vertices):
    """
    This function proves if a points is envolved in a polygone
    
    @param coords: x&y-coord of the point
    @type coords: Tupel(float,float)
    @param vertices: list of points, which defines a polygon
    @type vertices: [Tupel(float,float),]

    @return: true if point is inside
             false if point is outside or on edge
    """
    poly=vertices
    x=coords[0]
    y=coords[1]
    n = len(poly)
    inside =False

    p1x, p1y = poly[0]
    for i in range(n + 1):
      p2x, p2y = poly[i % n]
      if y > min(p1y , p2y):
        if y <= max(p1y , p2y):
          if x <= max(p1x , p2x):
            if p1y != p2y:
              xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xinters:
              inside = not inside
        p1x, p1y = p2x, p2y

    return inside
  
    
  def distToPolygon(self, node, vertices):
    """
    Function that returns the distance of the given node to the given polygon.
    
    @param node: The node to which the distance is calculated
    @type node: osmData.Node
    @param vertices: list of points, which defines a polygon
    @type vertices: [Tupel(float,float),]
    
    @return minDist: The distance to the given node
             if minDist>0 point is outside
             if mindDist=0 point is on edge
             if point is inside: -1 
             if the placemark contains no polygon: -2
    """
    if not isinstance(node, Node):
      raise TypeError("distToPolygon only accepts Nodes from type osmData.Node")
    if not self.hasPolygon():
      return -2.0
    if self._isPointInsidePolygon(node.coords,vertices):
      return -1.0  
    return self.distToLines(node,vertices)
  
  def distToLines(self,node,vertices):
    """
    Function that returns the shortest distance of the given node to a list of edges.
    
    @param node: The node to which the distance is calculated
    @type node: osmData.Node
    @param vertices: list of points, which defines a polygon
    @type vertices: [Tupel(float,float),]
    
    @return minDist: The distance to the given node
    """
    if not isinstance(node, Node):
      raise TypeError("distToPolygon only accepts Nodes from type osmData.Node")
    minDist=sys.float_info.max
    for s in self._sides(vertices):
      dist=self._distPointLine(node.lat,node.lon,s[0][0],s[0][1],s[1][0],s[1][1])
      if dist<minDist:
        minDist=dist
    return minDist
  
  
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