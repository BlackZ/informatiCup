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
from isySUR import isyUtils

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
      This function returns the ids of the nodes and its distance which are closest to the given point 
      
      @param point: The point - (lat, lon) - for which the function has
                    to compute the closest node.
      @type point: Tuple(float,float)
  
      @param tags: A dictionary of tags, given as a key value pair, which
                  will be used to filter the nodes. You can use * as wildcard
                  for the value or key but NOT both.
                  
                  e.g. dict("type":"xyz") or dict("type":"*")               
      @type tags: dict(str:str)
      
      @param otherNodes: Use only this nodes, given by a list of
                             its IDs, to find the nearest relation.                       
      @type otherNodes: [str,]
      
      @return: The function returns a list distanceResult-Objects (e.g [distObj1,distObj2,...])
              which holds the following informations:
              
              - distance (float): If an object is found, it contains the
                                  distance to the nearest object
    
              - nearestObj (str, type):   it contains the ID and the type
                                          of the nearest object
                                        
                                        For example:
                                          found object: ("1", osmData.Node)
                                        
              - nearestSubObj [(str, type)]:  Is empty: [("-1",None)]
          If nothing is found, the resulting list is empty.
      @rtype: [osmData.distanceResult,..]
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestNode only accepts a dict to filter nodes")
    if not isinstance(otherNodes,types.ListType):
      raise TypeError("getNearestNode only accepts a list of other nodes")
    
    nearestNodes=[]
    
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
        if tag=="*" and tags[tag]=="*":
          nodeOk=True
          break
        if tag=="*" and not tags[tag] in node.tags.values():
          nodeOk=False
          break
        if not node.tags.has_key(tag) or not (node.tags[tag]==tags[tag] or tags[tag]=="*"):
          nodeOk=False
          break
      if not nodeOk:
        continue
      try:
        distObj=node.getDistance(point)    # calculate distance
          
        # proove if the current node is the current nearest node
        if len(nearestNodes)==0 or distObj.distance<nearestNodes[0].distance:
          nearestNodes=[distObj]
        elif distObj.distance==nearestNodes[0].distance:
          nearestNodes.append(distObj)
      except TypeError:
        pass
    return nearestNodes 
  
  def getNearestWay(self, point, onlyPolygons,tags={}, otherWays=[]):
    """
      This function returns the ids of the ways, the distance which is closest to the given point.
      
      @param point: The point - (lat, lon) - for which the function has
                    to compute the closest way.
      @type point: Tuple(float,float)
      
      @param onlyPolygons: True for only using Ways with complete Polygons for computation
                           False for use all
      
      @type onlyPolygons: boolean
  
      @param tags: A dictionary of tags, given as a key value pair, which
                  will be used to filter the ways. You can use * as wildcard
                  for the value or key but NOT both.
                  
                  e.g. dict("type":"xyz") or dict("type":"*")       
      @type tags: dict(str:str)
      
      @param otherWays: Use only these ways, given by a list of
                             its IDs, to find the nearest way.                       
      @type otherWays: [str,]
      
      @return: The function returns a list of distanceResult-Objects (e.g [distObj1,distObj2,...])
              which holds the following informations:
              
              - distance (float): If an object is found, it contains the
                                  distance to the nearest object
    
              - nearestObj [(str, type)]: If one object is found, it contains the ID and
                                          the type of the nearest object
                                        
                                        For example:
                                          found object: ("1", osmData.Way)
                                        
              - nearestSubObj [(str, type)]:  If an object is found, it contains the IDs
                                            of the two Nodes, which defines the nearest Edge.
                                            There could be several edges, which have the same
                                            distance
                                            
                                            For example:
                                              found object: [(["1","2"], osmData.Node),..]
          If nothing is found, the resulting list is empty.
      @rtype: [osmData.distanceResult,..]
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestWay only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestWay only accepts a dict to filter nodes")
    if not isinstance(otherWays,types.ListType):
      raise TypeError("getNearestWay only accepts a list of other ways")
    
    nearestWays=[]
    
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
        if tag=="*" and tags[tag]=="*":
          wayOk=True
          break
        if tag=="*" and not tags[tag] in way.tags.values():
          wayOk=False
          break
        if not way.tags.has_key(tag) or not (way.tags[tag]==tags[tag] or tags[tag]=="*"):
          wayOk=False
          break
      if not wayOk:
        continue
      try:
        distObj=way.getDistance(point)       # calculate distance
        
        # proove if current way is the current nearest way
        if len(nearestWays)==0 or distObj.distance<nearestWays[0].distance:
          nearestWays=[distObj]
        elif distObj.distance==nearestWays[0].distance:
          nearestWays.append(distObj)
      except TypeError:
        pass
    return nearestWays
  
  def getNearestRelation(self, point, tags={}, otherRelations=[]):
    """
      This function returns the ids of the relation,its way and its distance which is closest to the given point 
      
      @param point: The point - (lat, lon) - for which the function has
                    to compute the closest relation.
      @type point: Tuple(float,float)
  
      @param tags: A dictionary of tags, given as a key value pair, which
                  will be used to filter the realtions. You can use * as wildcard
                  for the value or key but NOT both.
                  
                  e.g. dict("type":"multipolyon")  or dict("type":"*")         
      @type tags: dict(str:str)
      
      @param otherRelations: Use only this relations, given by a list of
                             its IDs, to find the nearest relation.                       
      @type otherRelations: [str,]
      
      @return: The function returns a list of distanceResult-Object (e.g [distObj1,distObj2,...])
              which holds the following informations:
              
              - distance (float): If an object is found, it contains the
                                  distance to the nearest object
    
              - nearestObj (str, type): If one object is found, it contains the ID and
                                        the type of the nearest object
                                        
                                        For example:
                                          found object: ("1", osmData.Relation)
                                        
              - nearestSubObj [(str, type)]:  If an object is found, it contains the ID
                                            and the type of the neares subobject in
                                            the relation.
                                          
                                            For example:
                                                found object: [("1", osmData.Relation),..]
          If nothing is found, the resulting list is empty.
      @rtype: [osmData.distanceResult,..]
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getNearestRelation only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(tags, dict) :
      raise TypeError("getNearestRelation only accepts a dict to filter nodes")
    if not isinstance(otherRelations,types.ListType):
      raise TypeError("getNearestRelation only accepts a list of other relations")
    
    nearestRels=[]
    
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
        if tag=="*" and tags[tag]=="*":
          relOk=True
          break
        if tag=="*" and not tags[tag] in rel.tags.values():
          relOk=False
          break
        if not rel.tags.has_key(tag) or not (rel.tags[tag]==tags[tag] or tags[tag]=="*"):
          relOk=False
          break
      if not relOk:
        continue
      
      distResult=rel.getDistance(point)
      if len(nearestRels)==0 or distResult.distance<nearestRels[0].distance:
        nearestRels=[distResult]
      elif distResult.distance==nearestRels[0].distance:
        nearestRels.append(distResult)
    
    # take only top-lvl relations
    newNearestRel=copy.deepcopy(nearestRels)
    for item in newNearestRel:
      if not self.relations[item.nearestObj[0]].parent==None:
        for item2 in nearestRels:
          if item2.nearestObj[0]==item.nearestObj[0]:
            idx=nearestRels.index(item2)      
            del nearestRels[idx]
      
    return nearestRels

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
    
  def getCoordinateString(self):
    """
      Returns a string representation of the coordinates for this node.
      
      @return: A String with lon, lat. Both with 8 trailing digits
    """
    return "%.8f,%.8f" % (self.lon, self.lat)
    
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
      
      @return: (lat, lon) as tupel
      @rtype: Tupel(float,float)
    """
    return (self.lat,self.lon)
  
  def getDistance(self, point):
    """
      This function computes the distance between two points
      
      @param point: the point the distance should be computed with
      @type point: tuple of latitude and longitude (float,float)
      
      @return: The function returns a distanceResult-Object which holds the
              following informations:
              
              - distance (float): Distance between the current and the given point
    
              - nearestObj (str, type): The current node
                                          For example: ("1", osmData.Node)
                                        
              - nearestSubObj [(str, type)]:  is empty: [("-1", None)]
      @rtype: osmData.distanceResult
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("distToNode only accepts Tupels from type types.TupelType with 2 Entries from type float")
    tmpPoint=isyUtils.getXYpos(isyUtils._relativeNullPoint,point)
    ownPoint=isyUtils.getXYpos(isyUtils._relativeNullPoint,(self.lat,self.lon))

    return distanceResult(round(math.hypot(tmpPoint[0] - ownPoint[0], tmpPoint[1] - ownPoint[1]),8),(self.id,self.__class__))
  
class Way(object):
  
  def __init__(self, identifier, refs, tags, osmObj):
    """
      Basic class containing an osm Way
      
      Parameters
      ==========
    
      @param identifier: The id of the way as a string
      
      @param refs: An ordered list of node id's that make up the way
      @type refs: [str,..]
      
      @param tags: A dictionary containing all the tags for the way
      @type tags: dict(str:str,..)
      
      @param osmObj: Reference to the osmObj, this way is included in.
      @type osmObj: osmData.OSM
    """
    self.id = identifier
    if not isinstance(refs, list):
      raise TypeError("refs must be a list of id's")
    self.refs = refs
    if not isinstance(tags, dict):
      raise TypeError("tags must be a dictionary")
    self.tags = tags
    if not isinstance(osmObj, OSM):
      raise TypeError("osmObj must be a OSM object")
    self.osmObj=osmObj
  
  def isPolygon(self):
    """
      This functions prooves if the Way is a polygon
      
      @return: true if polygon exists
      @rtype: boolean
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
  
  def _sides(self):
    """
      This function returns a list of lists of tuples, which describes all edges of the polygone
      
      @return: edgeList: a list of lists of tuples (e.g. [[(0,0),(0,1)],[(0,1),(1,1)]]) a sublist represents an edge 
      @rtype: [[Tupel(float,float),Tupel(float,float)],..]
    """
    edgeList = []
    args = self._vertices()
    for i in xrange(-len(args), -1):
      edgeList.append([args[i], args[i + 1]])
    return edgeList
  
  def _vertices(self):
    """
      This function converts the points contained by node objects to a list of tuples
      
      @return: listOfPoints: a list of tuples, where each tuple reprent a point (e.g. [(0,0),(0,1),(1,1),(1,0)])
      @rtype: [Tupel(float,float),..]
    """
    listOfPoints=[]
    for n in self.osmObj.ways[self.id].refs:
      listOfPoints.append(self.osmObj.nodes[n].coords)
    return listOfPoints
  
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
      @rtype: float
    """
    dx = x2 - x1
    dy = y2 - y1
    if dx == dy == 0:  # the segment's just a point
      return math.hypot(px - x1, py - y1)
  
    # Calculate the t that minimizes the distance.
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
  
    # See if this represents one of the segments
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
  
    return round(math.hypot(dx, dy),8)
  
  
  def isInside(self, point, vertices=[]):
    """
      This function proves if a points is envolved in a polygone
      
      @param point: x and y-coord of the point
      @type point: Tupel(float,float)
      
      @param vertices: list of points to calculate with (e.g used for combined polygons)
      @type vertices: [Tupel(float,float),..]
  
      @return: true if point is inside
               false if point is outside or on edge or way isn't a polygon
      @rtype: boolean
    """
    if len(vertices)==0:  
      vertices=self._vertices()
      if not self.isPolygon():
        return False
    else:
      if not vertices[0]==vertices[-1]:
        return False
            
    cn = 0    # the crossing number counter

    # loop through all edges of the polygon
    for i in range(len(vertices)-1):   # edge from vertices[i] to vertices[i+1]
      tmpPoint=isyUtils.getXYpos(isyUtils._relativeNullPoint,point)
      vi=isyUtils.getXYpos(isyUtils._relativeNullPoint,vertices[i])
      vii=isyUtils.getXYpos(isyUtils._relativeNullPoint,vertices[i+1])
      if ((vi[1] <= tmpPoint[1] and vii[1] > tmpPoint[1])   # an upward crossing
        or (vi[1] > tmpPoint[1] and vii[1] <= tmpPoint[1])):  # a downward crossing
        # compute the actual edge-ray intersect x-coordinate
        vt = (tmpPoint[1] - vi[1]) / float(vii[1] - vi[1])
        if tmpPoint[0] < vi[0] + vt * (vii[0] - vi[0]): # coords[0] < intersect
          cn += 1  # a valid crossing of y=coords[1] right of coords[0]

    return cn % 2 == 1   # 0 if even (out), and 1 if odd (in)

  
  def getDistance(self, point):
    """
      Function that returns the distance of the given point to the current way.
      
      @param point: The point(lat,lon) to which the distance is calculated
      @type point: Tuple(float,float)
      
      @return: The function returns a distanceResult-Object which holds the
               following informations:
              
               - distance (float): The distance between the current way and the given point
    
               - nearestObj [(str, type)]: The current way
                                           For example: [("1", osmData.Way)]
                                        
               - nearestSubObj [(str, type)]:  The edge from the current way which is closest
                                               For example: [(["1","2"], osmData.Node)]
      @rtype: osmData.distanceResult
    """
    if not isinstance(point, types.TupleType) or not len(point)==2:
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")
    if not isinstance(point[0], float) or not isinstance(point[1], float) :
      raise TypeError("getDistance only accepts Tupels from type types.TupelType with 2 Entries from type float")
    
    result=distanceResult(sys.float_info.max,(self.id,self.__class__))
    for s in self._sides():
      tmpPoint=isyUtils.getXYpos(isyUtils._relativeNullPoint,point)
      s0=isyUtils.getXYpos(isyUtils._relativeNullPoint,s[0])
      s1=isyUtils.getXYpos(isyUtils._relativeNullPoint,s[1])
      dist=self._distPointLine(tmpPoint[0],tmpPoint[1],s0[0],s0[1],s1[0],s1[1])
      if dist<result.distance:
        result.distance=dist
        result.nearestSubObj=[(s,self.osmObj.nodes[self.refs[0]].__class__)]
      elif dist==result.distance:
        result.nearestSubObj+=[(s,self.osmObj.nodes[self.refs[0]].__class__)]
    return result
  
class Relation(object):
  
  def __init__(self, identifier, members, tags, osmObj):
    """
      Basic class containing an osm Relation
      
      Parameters
      ==========      
      
      @param identifier: The id of the relation.
      @type identifier: any type      
      
      @param members: The members of this relation.
      @type members: A list of tripel [membertype(e.g.  way), id of the member, addition tags (e.g. outer)]
      
      @param tags: A dictionary containing all the tags for the relation
      @type tags: {key: value,}
      
      @param osmObj: Reference to the osmObj, this way is included in.
      @type osmObj: osmData.OSM
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
    if not isinstance(osmObj, OSM):
      raise TypeError("osmObj must be a OSM object.")
    self.osmObj=osmObj
    self.parent=None
    
  def getDistance(self, point):
    """
      Function that returns the distance of the given point to the current relation.
      
      @param point: The point(lat,lon) to which the distance is calculated
      @type point: Tuple(float,float)
      
      @return: The function returns a distanceResult-Object which holds the
              following informations:
              
              - distance (float): Distance between the current and the given point
    
              - nearestObj (str, type): The current relation
                                          For example: ("1", osmData.Relation)
                                        
              - nearestSubObj [(str, type)]:  The nearestSubObject of the current relation
                                              For example: [("3", osmData.Way),..]
      @rtype: osmData.distanceResult
    """
    nearestElem=distanceResult(sys.float_info.max,(self.id,self.__class__))
    rel=self.osmObj.relations[self.id]
    globalMemb={"way":self.osmObj.ways,"node":self.osmObj.nodes,"relation":self.osmObj.relations}
    for m in rel.members:
      memb=globalMemb[m[0]][m[1]]
      if m[0]=="relation":
        memb.parent=self.id
        
      distResult=memb.getDistance(point)
      
      if distResult.distance<nearestElem.distance:
        nearestElem.distance=distResult.distance
        nearestElem.nearestSubObj=[distResult.nearestObj]
      elif distResult.distance==nearestElem.distance:
        nearestElem.nearestSubObj+=[distResult.nearestObj]
    return nearestElem
  
  def _searchForPolygons(self):
    """
      This function searches hidden polygons, which are defined by more then one way
      and saves them in the list "polygons" of the given relation
    """
    rel=self.osmObj.relations[self.id]
    for pos in ["outer","inner"]:     # only outer ways and inner ways together
      ways=[]
      for m in rel.members:           # collecting all ways
        if m[0]=="way" and m[2]==pos:
          ways.append(m[1])
      for w1_key in ways:             # for all ways proove if it could be completed to a polygon
        if not any([w1_key in x for x in rel.polygons]):
          tmpResult=[w1_key]
          tmpWays=copy.deepcopy(ways)   # make a deep copy of the remaining way-objects
          tmpWays.remove(w1_key)        # and delete the current way
          for i in range(0, len(tmpWays)):    # for each item of the remaining way-objects
            for w2_key in tmpWays:
              w2=self.osmObj.ways[w2_key]
              # is the last node-id of the last added way = first node-id of the next way
              if self.osmObj.ways[tmpResult[-1]].refs[-1]==w2.refs[0]:
                tmpResult.append(w2_key)
                tmpWays.remove(w2_key)
                break
          if self.osmObj.ways[tmpResult[0]].refs[0]==self.osmObj.ways[tmpResult[-1]].refs[-1]:    # complete polygon?
            rel.addPolygon(tmpResult)
  
  def isInside(self, point):
    """
      This function prooves, if a point is inside a relation.
      
      @param point: the point to proove
      @type point; Tuple(float,float)
      
      @return: the result e.g. (True,([1],osmData.Way)) or (True,([1,2,5],osmData.Way)) for polygon combinded of more then one way
      @rtype: Tupel(boolean,Tupel([str/int,..],osmData.Types))
    """
    rel=self.osmObj.relations[self.id]
    if len(rel.polygons)==0:
      rel._searchForPolygons()
      
    memb={"way":[],"node":[],"relation":[]}
    for m in rel.members:
      memb[m[0]].append(m[1])
      
    result=(sys.float_info.max,("-1",None))
    # proove all ways
    for w in memb["way"]:
      way=self.osmObj.ways[w]
      if any([w in x for x in rel.polygons]):
        vertices=[]
        if way.isPolygon():
          vertices=way._vertices()
        else:
          vertices=[z for y in rel.polygons for x in y for z in self.osmObj.ways[x]._vertices() if way.id in y]
        if len(vertices)>0 and way.isInside(point,vertices):
          distResult=way.getDistance(point)
          if result[0]>distResult.distance:
            result=(distResult.distance,([x for y in rel.polygons for x in y if way.id in y],way.__class__))
    # proove all relations
    for r in memb["relation"]:
      subRes=self.osmObj.relations[r].isInside(point)
      if result[0]>subRes[0]:
        result=(subRes[0],([r],self.osmObj.relations[r].__class__))
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
    
  def hasMember(self, memId):
    """
      Function to query if the given member is present in the relation
      
      @param memId: The member id that is to be tested.
      @type memId: Any type
      
      @return: True if this relation has got a member of the given id, else False
      @rtype: Boolean
    """
    for mem in self.members:
      if mem[1] == memId:
        return True
    return False
   
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
    
    @param nearestObj: the ID and type of the nearest object e.g. ("1",osmData.Relation)
    @type nearestObj: Tuple(str,type)
    
    @param nearestSubObj: (optional) the nearest subobject of the current
                          nearest object (a way which is a subobject of a relation)
                          e.g. [("2",osmData.Way),...]
    @type nearestSubObj: [Tuple(str,str)]
    """
    self.distance = distance
    self.nearestObj = nearestObj
    self.nearestSubObj = nearestSubObj
