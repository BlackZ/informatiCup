# -*- coding: utf-8 -*-

import requests
import osmData
import types

import xml.dom.minidom as dom
import xml.etree.cElementTree as ET

class osmAPI():
  
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def _getOsmRequestData(self, minLat, minLon, maxLat, maxLon, filterList):
    """
    Builds the paramter string for the OSM Request depending if a filterList is
    given or not.
    """
    if len(filterList) == 0:
      return {'data': '[out:xml][timeout:25];'\
              '(node[""=""]({minLat},{minLon},{maxLat},{maxLon});'\
              'way[""=""]({minLat},{minLon},{maxLat},{maxLon});'\
              'relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););'\
              '(._;>;); out body qt;'.format(**locals())} #out body;>;out body qt;'.format(**locals())}
    else:
      compactOverpassQLstring = '[out:xml][timeout:25];('
      for fil in filterList:
          if len(fil)==2:
            tmpFil=""
            for obj in fil[1]:
              tmpFil+="[" + obj + "]"
            compactOverpassQLstring += '%s%s(%s,%s,%s,%s);'% (fil[0], tmpFil, minLat, minLon, maxLat, maxLon)
      compactOverpassQLstring += ');(._;>;); out body qt;'
      return  {'data':compactOverpassQLstring}
      
  def getDataFromPoly(self, polyString):
    """
      Function to request parsed data from osm that is within the polygon given by the polyString
      
      @param polyString: String containing the outline of the polygon "lat1 lon1 lat2 lon2 ..."
      @type polyString: "String"
      
      @return: The parsed osmData
      @rtype: osmData.OSM
    """
    return self._parseDataET(requests.get(self.osmurl, params={'data':'(node(poly:"'+polyString+'");<;);(._;>;); out body qt;'}).content)


  def performRequest(self, boundingBox, filterList=[]):
    """
    This function requests data from openStreetMap
    @param boundingBox: a list of the points of the boundingBox [minLat,minLon,maxLat,maxLon]
    @param filterList: (optional) List of tupel of filter-rules e.g.[('way',['"amenity"="univerity"',..]),..]
                        or ('way',['"building"=""']) for some kind of wild-card
    @return: an request object with the data-xml in the content property
    """
    if not isinstance(filterList,types.ListType):
      raise TypeError('performRequest only accepts a list of filterrules')
    return self._parseDataET(
      requests.get(self.osmurl,
                    params=self._getOsmRequestData(boundingBox[0],
                                                   boundingBox[1],
                                                   boundingBox[2],
                                                   boundingBox[3],
                                                   filterList)).content)


  def _getTagsET(self, elem):
    res = {}
    for tag in elem.iter("tag"):
      res[tag.attrib["k"]] = tag.attrib["v"]
    return res

  def _getRefsET(self, elem):
    res = []
    for ref in elem.iter("nd"):
      res.append(ref.attrib["ref"])
      
    return res
    
  def _getMembersET(self, elem):
    res = []
    for mem in elem.iter("member"):
      res.append((mem.attrib["type"], mem.attrib["ref"], mem.attrib["role"]))
    return res

  def _parseDataET(self, obj):
    osmObj = osmData.OSM()
    
    root=ET.fromstring(obj)

    
    for node in root.iter("node"):
      nodeObj = osmData.Node(node.attrib["id"].encode('utf-8'), 
                             float(node.attrib["lat"]), 
                             float(node.attrib["lon"]), 
                             self._getTagsET(node))
      if osmObj.nodes.has_key(nodeObj.id):
        osmObj.nodes[nodeObj.id].tags = nodeObj.tags
      else:
        osmObj.addNode(nodeObj)
        
    for way in root.iter("way"):
      wayObj = osmData.Way(way.attrib["id"].encode('utf-8'), self._getRefsET(way), self._getTagsET(way), osmObj)
      if osmObj.ways.has_key(wayObj.id):
        if len(osmObj.ways[wayObj.id].refs) == 0:
          osmObj.ways[wayObj.id].refs = wayObj.refs
        if len(osmObj.ways[wayObj.id].tags) == 0:
          osmObj.ways[wayObj.id].tags = wayObj.tags
      else:
        osmObj.addWay(wayObj)

    for relation in root.iter("relation"):
      relationObj = osmData.Relation(relation.attrib["id"].encode('utf-8'), 
                                     self._getMembersET(relation),
                                     self._getTagsET(relation),
                                     osmObj)
      if osmObj.relations.has_key(relationObj.id):
        if len(osmObj.relations[relationObj.id].members) == 0:
          osmObj.relations[relationObj.id].members = relationObj.members
        if len(osmObj.relations[relationObj.id].tags) == 0:
          osmObj.relations[relationObj.id].tags = relationObj.tags
      else:
        osmObj.addRelation(relationObj)
      

    return osmObj    
  

  def _parseData(self, obj):
    """
    Splits the incoming OSM Date into Nodes, Ways and Relations
    and stores it into an OSMObject for further calculations.
    """

    osmObj=osmData.OSM()
    
    data = dom.parseString(obj)
    
    pass
    for node in data.getElementsByTagName('node'):      
      node_id = node.getAttribute('id').encode('utf-8')
      
      if (osmObj.nodes.has_key(node_id)):
        if len(osmObj.nodes[node_id].tags) == 0:
          osmObj.nodes[node_id].tags = self._getTags(node)
      else:
        node_tags = self._getTags(node)
        
        nodeObj=osmData.Node(node_id,
                             float(node.getAttribute('lat')),
                             float(node.getAttribute('lon')),
                             node_tags)
        osmObj.addNode(nodeObj)
      node.unlink()
      
    for way in data.getElementsByTagName('way'):
      way_id = way.getAttribute('id').encode('utf-8')
      
      if (osmObj.ways.has_key(way_id)):
        if len(osmObj.ways[way_id].refs) == 0:
          osmObj.ways[way_id].refs = self._getRefs(way)
        if len(osmObj.ways[way_id].tags) == 0:
          osmObj.ways[way_id].tags = self._getTags(way)
      
      else:
        if way.hasChildNodes():
          way_refs = self._getRefs(way)
          way_tags = self._getTags(way)
        
          wayObj = osmData.Way(way_id, way_refs, way_tags, osmObj)  
          osmObj.addWay(wayObj)
      way.unlink()
      
    for relation in data.getElementsByTagName('relation'):
      rel_id = relation.getAttribute('id').encode('utf-8')
      
      if (osmObj.relations.has_key(rel_id)):
        if len(osmObj.relations[rel_id].members) == 0:
          osmObj.relations[rel_id].refs = self._getMembers(relation)
        if len(osmObj.relations[rel_id].tags) == 0:
          osmObj.relations[rel_id].tags = self._getTags(relation)

      else:
        if relation.hasChildNodes() :
          rel_members = self._getMembers(relation)
          rel_tags = self._getTags(relation) 

          relObj = osmData.Relation(rel_id, rel_members, rel_tags, osmObj)
          osmObj.addRelation(relObj)
      relation.unlink()

    del data
    return osmObj

  def _getTags(self, elem):
    """
    Returns a dictionary of tags for a given element.    
    """
    tags = {}
    for element in elem.getElementsByTagName('tag'):
        tags[element.getAttribute('k').encode('utf-8')] = element.getAttribute('v').encode('utf-8')
    
    return tags
  
  def _getRefs(self, node):
    """
    Returns a list of refereences for a given element.
    """
    refs = []
    for element in node.getElementsByTagName('nd'):
      refs.append(element.getAttribute('ref').encode( "utf-8" ))
      
    return refs

  def _getMembers(self, rel):
    """
    Returns a list of members for a given relation. 
    """
    members = []
    for element in rel.getElementsByTagName('member'):
      type = element.getAttribute('type').encode("utf-8")
      ref = element.getAttribute('ref').encode("utf-8")
      role = element.getAttribute('role').encode("utf-8")
      members.append((type, ref, role))
      
    return members
