# -*- coding: utf-8 -*-
"""
Base class that builds a connection to the Openstreetmap API.
"""
#@author: jhemming & tschodde

import requests
import osmData
import types

import xml.etree.cElementTree as ET

class osmAPI():
  
  def __init__(self):
    """
    Constructor of the osmAPI making a conntection to Openstreetmap.
    """
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def _getOsmRequestData(self, minLat, minLon, maxLat, maxLon, filterList):
    """
      Builds the paramter string for the OSM Request depending if a filterList is
      given or not.
      
      @param minLat: the left bottom corner lat value of the bounnding box
      @type minLat: float
      
      @param minLon: the left bottom corner lon value of the bounnding box
      @type minLon: float
      
      @param maxLat: the right upper corner lat value of the bounnding box
      @type maxLat: float
      
      @param maxLon: the right upper corner lon value of the bounnding box
      @type maxLon: float
      
      @param filterList: List of tupel of filter-rules e.g.[('way',['"amenity"="univerity"',..]),..]
                          or ('way',['"building"=""']) for some kind of wild-card
      @type filterList: [Tupel(str,[str,..])]
      
      @return returns the request-string, which could be send to the openStreetMap-Api
      @rtype: str
    """
    if len(filterList) == 0:
      return {'data': '[out:xml][timeout:35];'\
              '(node[""=""]({minLat},{minLon},{maxLat},{maxLon});'\
              'way[""=""]({minLat},{minLon},{maxLat},{maxLon});'\
              'relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););'\
              '(._;>>;); out body qt;'.format(**locals())} #out body;>;out body qt;'.format(**locals())}
    else:
      compactOverpassQLstring = '[out:xml][timeout:35];('
      for fil in filterList:
          if len(fil)==2:
            tmpFil=""
            for obj in fil[1]:
              tmpFil+="[" + obj + "]"
            compactOverpassQLstring += '%s%s(%s,%s,%s,%s);'% (fil[0], tmpFil, minLat, minLon, maxLat, maxLon)
      compactOverpassQLstring += ');(._;>>;); out body qt;'
      return  {'data':compactOverpassQLstring}
      
  def getDataFromPoly(self, polyString):
    """
      Function to request parsed data from osm that is within the polygon given by the polyString
      
      @param polyString: String containing the outline of the polygon "lat1 lon1 lat2 lon2 ..."
      @type polyString: "String"
      
      @return: The parsed osmData
      @rtype: osmData.OSM
    """
    return self._parseData(requests.get(self.osmurl, params={'data':'(node(poly:"'+polyString+'");<;);(._;>;); out body qt;'}).content)


  def performRequest(self, boundingBox, filterList=[]):
    """
      This function requests data from openStreetMap
      @param boundingBox: a list of the points of the boundingBox [minLat,minLon,maxLat,maxLon]
      @type boundingBox: [float,float,float,flaot]
      
      @param filterList: (optional) List of tupel of filter-rules e.g.[('way',['"amenity"="univerity"',..]),..]
                          or ('way',['"building"=""']) for some kind of wild-card
      @type filterList: [Tupel(str,[str,..])]
      
      @return: an request object with the data-xml in the content property
    """
    if not isinstance(filterList,types.ListType):
      raise TypeError('performRequest only accepts a list of filterrules')
    return self._parseData(
      requests.get(self.osmurl,
                    params=self._getOsmRequestData(boundingBox[0],
                                                   boundingBox[1],
                                                   boundingBox[2],
                                                   boundingBox[3],
                                                   filterList)).content)


  def _getTags(self, elem):
    """
      Private function to get the tags present in an element.
      
      @param elem: Element whose tags are to be extracted.
      @type elem: ET.Element
      
      @return: A dictionary containing all tags as key:value pairs
      @rtype: {"k":"v",}
    """
    res = {}
    for tag in elem.iter("tag"):
      res[tag.attrib["k"]] = tag.attrib["v"]
    return res

  def _getRefs(self, elem):
    """
      Private function to get all references present in an element.
      
      @param elem: The element whose references are to be extracted.
      @type elem: ET.Element
      
      @return: A list of all references contained in the given element.
      @rtype: [String,]
    """
    res = []
    for ref in elem.iter("nd"):
      res.append(ref.attrib["ref"])
      
    return res
    
  def _getMembers(self, elem):
    """
      Private function to get all the members present in an element.
      
      @param elem: The element whose members are to be extracted.
      @type elem: ET.Element
      
      @return: A list tripel, containing the type, the referenceId and the role of all members.
      @rtype: [(String,String,String),]
    """
    res = []
    for mem in elem.iter("member"):
      res.append((mem.attrib["type"], mem.attrib["ref"], mem.attrib["role"]))
    return res

  def _parseData(self, obj):
    """
      Private function to parse the osm data string into our OSM data structure.
      
      @param obj: The osm data XML-string
      @type: String
      
      @return: The parsed osm data in the OSM data structur
      @rtype: osmData.OSM
    """
    print "length data", len(obj)
#    print obj
    osmObj = osmData.OSM()
    
    root=ET.fromstring(obj)

    
    for node in root.iter("node"):
      nodeObj = osmData.Node(node.attrib["id"].encode('utf-8'), 
                             float(node.attrib["lat"]), 
                             float(node.attrib["lon"]), 
                             self._getTags(node))
      if nodeObj.id == "1246147":
        print "node present!"
      if osmObj.nodes.has_key(nodeObj.id):
        osmObj.nodes[nodeObj.id].tags = nodeObj.tags
      else:
        osmObj.addNode(nodeObj)
        
    for way in root.iter("way"):
      wayObj = osmData.Way(way.attrib["id"].encode('utf-8'), self._getRefs(way), self._getTags(way), osmObj)
      if osmObj.ways.has_key(wayObj.id):
        if len(osmObj.ways[wayObj.id].refs) == 0:
          osmObj.ways[wayObj.id].refs = wayObj.refs
        if len(osmObj.ways[wayObj.id].tags) == 0:
          osmObj.ways[wayObj.id].tags = wayObj.tags
      else:
        osmObj.addWay(wayObj)

    for relation in root.iter("relation"):
      relationObj = osmData.Relation(relation.attrib["id"].encode('utf-8'), 
                                     self._getMembers(relation),
                                     self._getTags(relation),
                                     osmObj)
      if osmObj.relations.has_key(relationObj.id):
        if len(osmObj.relations[relationObj.id].members) == 0:
          osmObj.relations[relationObj.id].members = relationObj.members
        if len(osmObj.relations[relationObj.id].tags) == 0:
          osmObj.relations[relationObj.id].tags = relationObj.tags
      else:
        osmObj.addRelation(relationObj)

    return osmObj    

