# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:31:52 2014
Basic class that holds the osm-data (consisting of basing elements)
@author: adreyer
"""
import sys
import math
import types
import copy

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
  
  def getNearestNode(self, coords, tags={}, otherNodes=[]):
    """
    This function returns the nearest node and its distance given a point and an optional list of tags
    
    @param coords: a point for which the nearest node should be found
    @type coords: Tupel(float,float)
    
    @param tags: a list of tags for filtering the nodes e.g. {"":""}
    @type tags: dict(str:str)
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestNode only accepts a dict to filter nodes")
    
    nearestNode=distanceResult(sys.float_info.max,("-1",None))
    
    nodes=[]
    if len(otherNodes)>0:
      nodes==otherNodes
    else:
      nodes=self.nodes
    
    for n in nodes:
      node=self.nodes[n]
      nodeOk=True
      for tag in tags:
        if not node.tags.has_key(tag) or not node.tags[tag]==tags[tag]:
          nodeOk=False
      if not nodeOk:
        continue
      try:
        dist=node.distToNode(coords)
        if dist<nearestNode.distance:
          nearestNode.distance=dist
          nearestNode.nearestObj=(node.id,"node")
      except TypeError:
        pass
    return nearestNode 
  
  def getNearestWay(self, coords, onlyPolygons,tags={}, otherWays=[]):
    """
    This function returns the id of the polygon(way) and its distance which is closest to the given node
    
    @param coords: point for which the function have to compute closest polygon
    @type coords: Tuple(float,float)
    @param onlyPolygons: prove only distance to way with complete polygons?
    @type onlyPolygons: boolean
    @param tags: list of tags which will be used to filter the ways
    @type tags: dict(str:str)
    @param otherWays: use this ways to find nearest way
    @type otherWays: [str,]
    
    @return Tupel(id,distance)
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestWay only accepts a dict to filter nodes")
    
    nearestWay=distanceResult(sys.float_info.max,("-1",None))
    
    ways=[]
    if len(otherWays)>0:
      ways=otherWays
    else:
      ways=self.ways
    
    for n in ways:
      way=self.ways[n]
      wayOk=True
      if onlyPolygons and not way.hasPolygon():
        continue
      for tag in tags:
        if not way.tags.has_key(tag) or not way.tags[tag]==tags[tag]:
          wayOk=False
      if not wayOk:
        continue
      try:
        dist=way.getDistance(coords,self._vertices(way.refs))
        if dist<nearestWay.distance:
          nearestWay.distance=dist
          nearestWay.nearestObj=(way.id,"way")
      except TypeError:
        pass
    return nearestWay
  
  #======================================
  #TODO: Beachte auch zusammengesetze Polygone!
  #======================================
  def getNearestRelation(self, coords, tags={}):
    """
    This function returns the ids of the relation,its way and its distance which is closest to the given node 
    
    @param coords: point for which the function have to compute closest polygon
    @type coords: Tuple(float,float)
    @param onlyPolygons: prove only distance to way with complete polygons?
    @type onlyPolygons: boolean
    @param tags: list of tags which will be used to filter the ways
    @type tags: dict(str:str)
    
    @return Tupel(Tupel(rel_id,way_id),distance)
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestRelation only accepts a dict to filter nodes")
    
    nearestRel=distanceResult(sys.float_info.max,("-1",None))
    
    for r in self.relations:
      rel=self.relations[r]

      relOk=True
      for tag in tags:
        if not rel.tags.has_key(tag) or not rel.tags[tag]==tags[tag]:
          relOk=False
      if not relOk:
        continue
      
      memb={"way":[],"node":[],"relation":[]}
      for m in rel.members:
        memb[m[0]].append(m[1])
        
      nearestNode=distanceResult(sys.float_info.max,("-1",None))
      nearestWay=distanceResult(sys.float_info.max,("-1",None))
      nearestSubRel=distanceResult(sys.float_info.max,("-1",None))
      if len(memb["node"])>0:
        nearestNode=self.getNearestNode(coords, {}, memb["node"])
      if len(memb["way"])>0:
        nearestWay=self.getNearestWay(coords, False ,{}, memb["way"])
      if len(memb["relation"])>0:
        nearestSubRel=self.getNearestRelation(coords,tags)
      
      for obj in [nearestNode,nearestWay,nearestSubRel]:
        if obj.distance<nearestRel.distance:
          nearestRel.distance=obj.distance
          nearestRel.nearestSubObj=obj.nearestObj
          nearestRel.nearestObj=(rel.id,"relation")
          nearestRel.insidePolygon=obj.insidePolygon
    return nearestRel
  
  def _searchForPolygons(self,rel):
    """
    This function searches hidden polygons, which are defined by more then one way
    """
    if not isinstance(rel, Relation) :
      raise TypeError("_searchForPolygons only accepts an object with type osmData.Relation")
    for pos in ["outer","inner"]:
      ways=[]
      for m in rel.members:
        if m[0]=="way" and m[2]==pos:
          ways.append(str(m[1]))
      for w1_key in ways:
        w1=self.ways[w1_key]
        tmpResult=[w1_key]
        tmpWays=copy.deepcopy(ways)
        tmpWays.remove(w1_key)
        tmpLen=len(tmpWays)-1
        for i in range(0, tmpLen):
          for w2_key in tmpWays:
            w2=self.ways[w2_key]
            if self.ways[tmpResult[-1]].refs[-1]==w2.refs[0]:
              tmpResult.append(w2_key)
              tmpWays.remove(w2_key)
              break
        if self.ways[tmpResult[0]].refs[0]==self.ways[tmpResult[-1]].refs[-1]:
          rel.addPolygon(tmpResult)
          for res in tmpResult:
            ways.remove(res)
          
  
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
  
  def distToNode(self, coords):
    """
    This function computes the distance between two points
    
    @param cords: the point the distance should be computed with
    @type node: tuple of latitude and longitude (float,float)
    
    @return distance between both nodes
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    return math.hypot(coords[0] - self.lat, coords[1] - self.lon)
  
  
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
    
    @param vertices: all points of the polygon
    @type vertices: [(float,float),...]
    
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
  
  def _isPointInsidePolygon(self, coords, vertices):
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
  
    
  def getDistance(self, coords, vertices):
    """
    Function that returns the distance of the given node to the given way.
    
    @param coords: The point(lat,lon) to which the distance is calculated
    @type coords: Tuple(float,float)
    @param vertices: list of points, which defines a way
    @type vertices: [Tupel(float,float),]
    
    @return minDist: The distance to the given node
             if minDist>0 point is outside
             if mindDist=0 point is on edge
             if point is inside: -1 
             if the placemark contains no polygon: -2
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")    
    minDist=sys.float_info.max
    for s in self._sides(vertices):
      dist=self._distPointLine(coords[0],coords[1],s[0][0],s[0][1],s[1][0],s[1][1])
      if dist<minDist:
        minDist=dist
        
    if self.hasPolygon():
      if self._isPointInsidePolygon(coords,vertices):
        minDist=-minDist
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
    
    self.polygons = []    
  
  def addPolygon(self, nodeList):
    self.polygons.append(nodeList)
    
  def addPolygonList(self, polyList):
    #self.polygons = [tuple(poly) for poly in polyList]
    self.polygons=polyList
   
  def __eq__(self,other):   
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.members == other.members 
      and self.tags == other.tags)
   
  def __ne__(self,other):
    return not self.__eq__(other)
  
class distanceResult(object):
  def __init__(self, distance, nearestObj, nearestSubObj=("-1",None)):
    if distance<0:
      self.distance=-distance
      self.insidePolygon=True
    else:
      self.distance=distance
      self.insidePolygon=False
    self.nearestObj=nearestObj
    self.nearestSubObj=nearestSubObj
  
  @property
  def distance(self):
    return self.__distance

  @distance.setter
  def distance(self,distance):
    if distance<0:
      self.__distance=-distance
      self.insidePolygon=True
    else:
      self.__distance=distance
      self.insidePolygon=False