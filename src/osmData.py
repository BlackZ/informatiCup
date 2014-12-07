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
    """
      Constructor for the osm data object. 
      
      Initialises the dictionaries for the nodes, ways and relations that will be 
      contained in this osmObject.
      
    """
    self.nodes = {}
    self.ways = {}
    self.relations = {}
    
    self.visitedRelations={}
    
  def addNode(self, node):
    """
      Function to add a node to this osm object.
      
      @param relation: The node object that is to be added.
      
      @raise TypeError: TypeError is raised when something other than a node is passed.
    """
    if isinstance(node,Node):
      self.nodes[node.id] = node
    else:
      raise TypeError("addNode only accepts nodes.")
      
  def addNodeList(self, nodeList):
    """
      Function to add a list of nodes to this osm object.
      
      @param nodeList: The list of node objects that are to be added.
    """
    for node in nodeList:
      self.addNode(node)
    
  def addWay(self, way):
    """
      Function to add a way to this osm object.
      
      @param relation: The way object that is to be added.
      
      @raise TypeError: TypeError is raised when something other than a way is passed.
    """
    if isinstance(way,Way):
      self.ways[way.id] = way
    else:
      raise TypeError("addWay only accepts ways.")
    
  def addRelation(self,relation):
    """
      Function to add a relation to this osm object.
      
      @param relation: The relation object that is to be added.
      
      @raise TypeError: TypeError is raised when something other than a relation is passed.
    """
    if isinstance(relation,Relation):
      self.relations[relation.id] = relation
    else:
      raise TypeError("addRelation only accepts relations.")
      
  def __eq__(self, other):
    """
      Override of the equal method for OSM.
      
      Equality is based on the equality of the three dictionaries nodes, ways and relations
      
      @param other: The other osm object that this object is to be compared with.
      
      @return: True if the other object is equal to this object, else False.
      @rtype: Boolean
    """
    if not isinstance(other, self.__class__):
      return False
    
    return (self.nodes == other.nodes 
      and self.ways == other.ways
      and self.relations == other.relations)

  def __ne__(self,other):
    """
      Override of the not equal method for OSM.
      
      @param other: The osm object that this object is to be compared with.
      
      @return: True if other is not equal to this object, else False.
      @rtype: Boolean
    """
    return not self.__eq__(other)
  
  def getNearestNode(self, point, tags={}, otherNodes=[]):
    """
    This function returns the nearest node and its distance given a point and an optional list of tags
    
    @param point: a point for which the nearest node should be found
    @type point: Tupel(float,float)
    
    @param tags: a list of tags for filtering the nodes e.g. {"":""}
    @type tags: dict(str:str)
    
    @param otherNodes: use this nodes to find nearest node
    @type otherNodes: [str,]
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestNode only accepts a dict to filter nodes")
    
    nearestNode=distanceResult(sys.float_info.max,[("-1",None)])
    
    nodes=[]
    if len(otherNodes)>0:
      nodes==otherNodes
    else:
      nodes=self.nodes
    
    for n in nodes:             # for all nodes
      node=self.nodes[n]
      
      # proove if current node fullfill all filter-rules 
      nodeOk=True
      for tag in tags:
        if not node.tags.has_key(tag) or not node.tags[tag]==tags[tag]:
          nodeOk=False
          break
      if not nodeOk:
        continue
      try:
        if node.distance==None:
          node.distance=node.distToNode(point)    # calculate distance
          
        # proove if the current node is the current nearest node
        if node.distance<nearestNode.distance:
          nearestNode.distance=node.distance
          nearestNode.nearestObj=[(node.id,node.__class__)]
        elif node.distance==nearestNode.distance:
          nearestNode.nearestObj.append(node.id,node.__class__)
          
      except TypeError:
        pass
    return nearestNode 
  
  def getNearestWay(self, point, onlyPolygons,tags={}, otherWays=[]):
    """
    This function returns the id of the polygon(way) and its distance which is closest to the given node
    
    @param point: point for which the function have to compute closest polygon
    @type point: Tuple(float,float)
    
    @param onlyPolygons: prove only distance to way with complete polygons?
    @type onlyPolygons: boolean
    
    @param tags: list of tags which will be used to filter the ways
    @type tags: dict(str:str)
    
    @param otherWays: use this ways to find nearest way
    @type otherWays: [str,]
    
    @return Tupel(id,distance)
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestWay only accepts a dict to filter nodes")
    
    nearestWay=distanceResult(sys.float_info.max,[("-1",None)])
    ways=[]
    if len(otherWays)>0:
      ways=otherWays
    else:
      ways=self.ways
    for n in ways:              # for all ways
      way=self.ways[n]
      
      # proove if current way fullfill all filter-rules
      wayOk=True
      if onlyPolygons and not way.isPolygon():
        continue
      for tag in tags:
        if not way.tags.has_key(tag) or not way.tags[tag]==tags[tag]:
          wayOk=False
          break
      if not wayOk:
        continue
      try:
        if way.distance==None:
          way.distance=way.getDistance(point,self._vertices(way.refs))       # calculate distance
        
        # proove if current way is the current nearest way
        # TODO: ggf nearestEdge einfügen als subobject
        if way.distance<nearestWay.distance:
          nearestWay.distance=way.distance
          nearestWay.nearestObj=[(way.id,way.__class__)]
        elif way.distance==nearestWay.distance:
          nearestWay.nearestObj.append((way.id,way.__class__))
      except TypeError:
        pass
    return nearestWay
  
  def getNearestRealtionOld(self, coords, tags={}, otherRelations=[]):
    """
    This function returns the ids of the relation,its way and its distance which is closest to the given node 
    
    @param coords: point for which the function have to compute closest polygon
    @type coords: Tuple(float,float)

    @param tags: list of tags which will be used to filter the ways
    @type tags: dict(str:str)
    
    @param otherRelations: use this relations to find nearest relation
    @type otherRelations: [str,]
    
    @return Tupel(Tupel(rel_id,way_id),distance)
    """
    if not isinstance(coords, types.TupleType) or not len(coords)==2:
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(coords[0], float) or not isinstance(coords[1], float) :
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestRelation only accepts a dict to filter nodes")
    
    nearestRel=distanceResult(sys.float_info.max,[("-1",None)])
    
    relations=[]
    if len(otherRelations)>0:
      relations=otherRelations
    else:
      relations=self.relations
    
    for r in relations:
      rel=self.relations[r]
      
      if len(rel.polygons)==0:
        self._searchForPolygons(rel)

      # does this relation fullfill all filter-rules?
      relOk=True
      for tag in tags:
        if not rel.tags.has_key(tag) or not rel.tags[tag]==tags[tag]:
          relOk=False
      if not relOk:
        continue
      
      # sort all members by type
      memb={"way":[],"node":[],"relation":[]}
      for m in rel.members:
        memb[m[0]].append(m[1])
      
      # init resultObjects for member-distances  
      nearestNode=distanceResult(sys.float_info.max,[("-1",None)])
      nearestWay=distanceResult(sys.float_info.max,[("-1",None)])
      nearestSubRel=distanceResult(sys.float_info.max,[("-1",None)])

      if len(memb["way"])>0:
        nearestWay=self.getNearestWay(coords, False ,{}, memb["way"])
      if len(memb["node"])>0:
        nearestNode=self.getNearestNode(coords, {}, memb["node"])
      # if the found way belongs to a polygon combined of several ways proove if point is inside and set flag
      for p in rel.polygons:
        if nearestWay.nearestObj[0] in p:
          ver=[]
          for w_k in p:
            w=self.ways[w_k]
            for n_k in w.refs:
              n_coords=self.nodes[n_k].coords
              if n_coords not in ver:
                ver.append(n_coords)
          ver.append(ver[0])
          if self.ways[nearestWay.nearestObj[0]]._isPointInsidePolygon(coords,ver):
            nearestWay.insidePolygon=True
              
      # if the nearestWay was a inner-polygon --> the point couldn't be inside that polygon
        for m in rel.members:
          if nearestWay.nearestObj[0]==m[1] and m[2]=="inner":
            nearestWay.insidePolygon=False
      # get all memberDistances      
      if len(memb["relation"])>0:
        nearestSubRel=self.getNearestRelation(coords,tags,memb["relation"],level=level+1)

        
      # find the neareast subobject to determine the distance of the relation to the given point
      for obj in [nearestNode,nearestWay,nearestSubRel]:
        if obj.distance<=nearestRel.distance:
          nearestRel.distance=obj.distance
          nearestRel.nearestSubObj=obj.nearestObj
          nearestRel.nearestObj=[(rel.id,rel.__class__)]      
    return nearestRel
  
  def getNearestRelation(self, point, tags={}, otherRelations=[], level=0):
    """
    This function returns the ids of the relation,its way and its distance which is closest to the given node 
    
    @param point: point for which the function have to compute closest polygon
    @type point: Tuple(float,float)

    @param tags: list of tags which will be used to filter the ways
    @type tags: dict(str:str)
    
    @param otherRelations: use this relations to find nearest relation
    @type otherRelations: [str,]
    
    @return Tupel(Tupel(rel_id,way_id),distance)
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestRelation only accepts a dict to filter nodes")
    
    nearestRel=distanceResult(sys.float_info.max,[("-1",None)])
    
    relations=[]
    if len(otherRelations)>0:
      relations=otherRelations
    else:
      relations=self.relations
    
    for r in relations:
      rel=self.relations[r]

      # does this relation fullfill all filter-rules?
      relOk=True
      for tag in tags:
        if not rel.tags.has_key(tag) or not rel.tags[tag]==tags[tag]:
          relOk=False
          break
      if not relOk:
        continue
      
      # sort all members by type
      memb={"way":[],"node":[],"relation":[]}
      for m in rel.members:
        memb[m[0]].append(m[1])
      
      # init resultObjects for member-distances  
      nearestNode=distanceResult(sys.float_info.max,[("-1",None)])
      nearestWay=distanceResult(sys.float_info.max,[("-1",None)])
      nearestSubRel=distanceResult(sys.float_info.max,[("-1",None)])

      # get all memberDistances      
      if len(memb["relation"])>0:
        nearestSubRel=self.getNearestRelation(point,tags,memb["relation"],level=level+1)
      if len(memb["way"])>0:
        nearestWay=self.getNearestWay(point, False ,{}, memb["way"])
      if len(memb["node"])>0:
        nearestNode=self.getNearestNode(point, {}, memb["node"])
        
      # find the neareast subobject to determine the distance of the relation to the given point
      for obj in [nearestNode,nearestWay,nearestSubRel]:
        if obj.distance<nearestRel.distance:
          nearestRel.distance=obj.distance
          nearestRel.nearestSubObj=obj.nearestObj
          nearestRel.nearestObj=[(rel.id,rel.__class__)]
        elif obj.distance==nearestRel.distance and not obj.nearestObj[0][0]=="-1":
          # if subobj already found, don't add
          if (rel.id in self.visitedRelations.keys()):
            if self.visitedRelations[rel.id]>level:
              continue
          nearestRel.nearestSubObj=nearestRel.nearestSubObj+obj.nearestObj
          nearestRel.nearestObj.append((rel.id,rel.__class__))
      rel.distance=min(nearestNode.distance,nearestWay.distance,nearestSubRel.distance)
      
      # only update if this is the a deeper appeareance of the item
      if (rel.id in self.visitedRelations.keys() and level>self.visitedRelations[rel.id]) or not rel.id in self.visitedRelations.keys():
        self.visitedRelations.update({rel.id:level})
        
    # del all items which are listed but are subitems
    if level==0:
      newNearestRel=copy.deepcopy(nearestRel) 
      for i in range(0,len(nearestRel.nearestObj)):
        if nearestRel.nearestObj[i][0] in self.visitedRelations.keys() and self.visitedRelations[nearestRel.nearestObj[i][0]]>0:
          idx=newNearestRel.nearestObj.index(nearestRel.nearestObj[i])
          del newNearestRel.nearestObj[idx]
          del newNearestRel.nearestSubObj[idx]
      return newNearestRel
    return nearestRel

  def _searchForPolygons(self,rel):
    """
    This function searches hidden polygons, which are defined by more then one way
    and saves them in the list "polygons" of the given relation
    
    @param rel: the relation object for which the function searches for polygons inside
    @type rel: osmData.Relation
    """
    if not isinstance(rel, Relation) :
      raise TypeError("_searchForPolygons only accepts an object with type osmData.Relation")
    for pos in ["outer","inner"]:     # only outer ways and inner ways together
      ways=[]
      for m in rel.members:           # collecting all ways
        if m[0]=="way" and m[2]==pos:
          ways.append(m[1])
      for w1_key in ways:             # for all ways proove if it could be completed to a polygon
        if not any([w1_key in x for x in rel.polygons]):
          w1=self.ways[w1_key]          # get polygon by id
          tmpResult=[w1_key]
          tmpWays=copy.deepcopy(ways)   # make a deep copy of the remaining way-objects
          tmpWays.remove(w1_key)        # and delete the current way
          for i in range(0, len(tmpWays)):    # for each item of the remaining way-objects
            for w2_key in tmpWays:
              w2=self.ways[w2_key]
              # is the last node-id of the last added way = first node-id of the next way
              if self.ways[tmpResult[-1]].refs[-1]==w2.refs[0]:
                tmpResult.append(w2_key)
                tmpWays.remove(w2_key)
                break
          if self.ways[tmpResult[0]].refs[0]==self.ways[tmpResult[-1]].refs[-1]:    # complete polygon?
            rel.addPolygon(tmpResult)
  
  def _vertices(self,nodeList):
    """
    This function converts the points contained by node objects to a list of tuples
    
    @return listOfPoints: a list of tuples, where each tuple reprent a point (e.g. [(0,0),(0,1),(1,1),(1,0)])
    """
    listOfPoints=[]
    for n in nodeList:
      listOfPoints.append(self.nodes[n].coords)
    return listOfPoints

class Node(object):
  
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
    self.id = identifier
    self.lat = float(lat)
    self.lon = float(lon)
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary.")
    self.tags = tags
    self.distance=None
    
  def getCoordinateString(self):
    return str(self.lat) + "," +str(self.lon)
    
  def __eq__(self,other):
    """
      Override of the equality method for node. 
      
      Equality is based on the equality of the id, longitude, latitude and the tags.
      
      @param other: The node this node is to be compared with.
      
      @return: True if the other node is equal to this node with respect to 
              the above mentioned fields, else False.
      @rtype: Boolean
    """
    if not isinstance(other,self.__class__):
      return False
    
    return (self.id == other.id 
      and self.lat == other.lat 
      and self.lon == other.lon
      and self.tags == other.tags)
      
  def __ne__(self,other):
    """
      Override of the not equal method for node.
      
      @param other: The node that this node is to be compared with.
      
      @return: True if other is not equal to this node, else False.
      @rtype: Boolean
    """
    return not self.__eq__(other)
  
  @property
  def coords(self):
    """
    This function-property returns latitude and longitude as tupel
    
    @return (lon,lat) as tupel
    """
    return (self.lat,self.lon)
  
  def distToNode(self, point):
    """
    This function computes the distance between two points
    
    @param point: the point the distance should be computed with
    @type point: tuple of latitude and longitude (float,float)
    
    @return distance between both nodes
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    return math.hypot(point[0] - self.lat, point[1] - self.lon)
  
class Way(object):
  
  def __init__(self, identifier, refs, tags):
    """
    Basic class containing an osm Way
    
    @param identifier: The id of the way as a string
    
    @param refs: An ordered list of node id's that make up the way
    
    @param tags: A dictionary containing all the tags for the way
    """
    self.id = identifier
    if not isinstance(refs, list):
      raise TypeError("refs must be a list of id's")
    self.refs = refs
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary")
    self.tags = tags
    self.distance=None
  
  def isPolygon(self):
    """
    This functions prooves if the Way is a polygon
    
    @return true if polygon exists
    """
    if len(self.refs)>=4 and self.refs[0]==self.refs[-1]:
      return True
    return False
  
  def __eq__(self,other):
    """
      Override of the equality method for way. 
      
      Equality is based on the equality of the id, the references and the tags.
      
      @param other: The relation this relation is to be compared with.
      
      @return: True if the other way is equal to this way in id, references and tags, else False.
      @rtype: Boolean
    """
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.refs == other.refs 
      and self.tags == other.tags)
      
  def __ne__(self,other):
    """
      Override of the not equal method for way.
      
      @param other: The way that this way is to be compared with.
      
      @return: True if other is not equal to this way, else False.
      @rtype: Boolean
    """
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
  
  def _isPointInsidePolygonOld(self,coords,vertices):
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
              print "test",p1x,p1y,p2x,p2y
              xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
              print xinters
            if p1x == p2x or x <= xinters:
              print "test"
              inside = not inside
        p1x, p1y = p2x, p2y
    print coords,vertices,inside
    return inside
  
  def _isPointInsidePolygon(self, point, vertices):
    """
    This function proves if a points is envolved in a polygone
    
    @param point: x&y-coord of the point
    @type point: Tupel(float,float)
    
    @param vertices: list of points, which defines a polygon
    @type vertices: [Tupel(float,float),]

    @return: true if point is inside
             false if point is outside or on edge
    """
    cn = 0    # the crossing number counter

    # repeat the first vertex at end if not already done
    #if not vertices[0]==vertices[-1]:
    #  vertices = tuple(vertices[:])+(vertices[0],)

    # loop through all edges of the polygon
    for i in range(len(vertices)-1):   # edge from vertices[i] to vertices[i+1]
        if ((vertices[i][1] <= point[1] and vertices[i+1][1] > point[1])   # an upward crossing
            or (vertices[i][1] > point[1] and vertices[i+1][1] <= point[1])):  # a downward crossing
            # compute the actual edge-ray intersect x-coordinate
            vt = (point[1] - vertices[i][1]) / float(vertices[i+1][1] - vertices[i][1])
            if point[0] < vertices[i][0] + vt * (vertices[i+1][0] - vertices[i][0]): # coords[0] < intersect
                cn += 1  # a valid crossing of y=coords[1] right of coords[0]

    return cn % 2 == 1   # 0 if even (out), and 1 if odd (in)

  
  def getDistance(self, point, vertices):
    """
    Function that returns the distance of the given node to the given way.
    
    @param point: The point(lat,lon) to which the distance is calculated
    @type point: Tuple(float,float)
    @param vertices: list of points, which defines a way
    @type vertices: [Tupel(float,float),]
    
    @return minDist: The distance to the given node
             if minDist>0 distance to the way-obj
             if mindDist=0 point is on edge
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")    
    minDist=sys.float_info.max
    for s in self._sides(vertices):
      dist=self._distPointLine(point[0],point[1],s[0][0],s[0][1],s[1][0],s[1][1])
      if dist<minDist:
        minDist=dist
        
    #if self.isPolygon():
    #  if self._isPointInsidePolygon(coords,vertices):
    #    minDist=-minDist
    return minDist
  
class Relation(object):
  
  def __init__(self, identifier, members, tags):
    """
    Basic class containing an osm Relation
    
    @param identifier: The id of the relation.
    
    @param members: The members of this relation.
    @type members: A list of tripel [membertype(e.g.  way), id of the member, addition tags (e.g. outer)]
    
    @param tags: A dictionary containing all the tags for the relation
    @type tags: {key: value,}
    """
    self.id = identifier
    if not isinstance(members, list):
      raise TypeError("members need to be a list of tripel")
    self.members = [tuple(m) for m in members]   
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary")
    self.tags = tags
    self.distance=None
    self.polygons = []    
  
  def isInside(self, point, osmObj):
    """
    This function prooves, if a point is inside a relation.
    
    @param point: the point to proove
    @type point; Tuple(float,float)
    
    @param osmObj: current osm-Object with all data about nodes,ways and relations
    @type osmObj: osmData.osm
    
    @return the result e.g. (True,([1],osmData.Way)) or (True,([1,2,5],osmData.Way)) for polygon combinded of more then one way
    """
    rel=osmObj.relations[self.id]
    if len(rel.polygons)==0:
      osmObj._searchForPolygons(rel)
      
    memb={"way":[],"node":[],"relation":[]}
    for m in rel.members:
      memb[m[0]].append(m[1])
      
    result=(sys.float_info.max,("-1",None))
    # proove all ways
    for w in memb["way"]:
      way=osmObj.ways[w]
      if any([w in x for x in rel.polygons]):
        vertices=[]
        if way.isPolygon:
          vertices=osmObj._vertices(way.refs)
        else:
          vertices=[osmObj._vertices[osmObj.ways[i].refs] for i in rel.polygons]
        if len(vertices)>0 and way._isPointInsidePolygon(point,vertices):
          dist=way.getDistance(point,vertices)
          if result[0]>dist:
            result=(dist,([x for y in rel.polygons for x in y if way.id in y],way.__class__))
    # proove all relations
    for r in memb["relation"]:
      subRes=osmObj.relations[r].isInside(point,osmObj)
      if result[0]>subRes[0]:
        result=(subRes[0],([r],osmObj.relations[r].__class__))
    result=(not result[1]==("-1",None),result[1])
    return result    
  
  def addPolygon(self, wayList):
    """
    Function to add a polygon to the relation.
    
    @param wayList: List of way ids that make up the polygon 
    @type wayList: A list of ids. The id's can be of any type but must match
                  the type of the actual objects.
    """
    self.polygons.append(wayList)
    
  def addPolygonList(self, polyList):
    """
      Function to add a list of polygons to the relation.
      
      @param polyList: List of polygons. A polygon is given by a list of way Ids 
                      that make up the polygon.
      @type polyList: A list of lists that contain way Ids.
    """
    self.polygons=polyList
   
  def __eq__(self,other):   
    """
      Override of the equality method for relations. 
      
      Equality is based on the equality of the id, the members and the tags.
      
      @param other: The relation this relation is to be compared with.
      
      @return: True if the other relation is equal to this relation in id, members and tags, else False.
      @rtype: Boolean
    """
    if not isinstance(other, self.__class__):
      return False
    
    return (self.id == other.id 
      and self.members == other.members 
      and self.tags == other.tags)
   
  def __ne__(self,other):
    """
      Override of the not equal method for relations.
      
      @param other: The relation that this relation is to be compared with.
      
      @return: True if other is not equal to this relation, else False.
      @rtype: Boolean
    """
    return not self.__eq__(other)
  
class distanceResult(object):
  def __init__(self, distance, nearestObj, nearestSubObj=[("-1",None)]):
    """
    Basic class containing the result of a distance calculation

    Parameters
    ==========
    
    @param distance: The distance to the nearestObj
    @type distance: float
    
    @param nearestObj: the id and type of the nearest object e.g. ("1","relation")
    @type nearestObj: Tuple(str,str)
    
    @param nearestSubObj: (optional) the nearest subobject of the current
                          nearest object (a way which is a subobject of a relation)
                          e.g. ("2","way")
    @type nearestSubObj: Tuple(str,str)
    """
    self.distance=distance
    self.nearestObj=nearestObj
    self.nearestSubObj=nearestSubObj
