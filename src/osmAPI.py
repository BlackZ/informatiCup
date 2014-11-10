# -*- coding: utf-8 -*-

import requests
import osmData

import xml.dom.minidom as dom

class osmAPI():
  
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def _getOsmRequestData(self, minLat, minLon, maxLat, maxLon, filterList):
    if len(filterList) == 0:
      return {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}
    else:
      compactOverpassQLstring = '[out:xml][timeout:25];('
      for fil in filterList:
          for obj in fil[0]:
              compactOverpassQLstring += '%s["%s"="%s"](%s,%s,%s,%s);' % (obj, fil[1],fil[2], minLat, minLon, maxLat, maxLon)
      compactOverpassQLstring += ');out body;>;out skel qt;'
      return  {'data':compactOverpassQLstring}


  def performRequest(self, boundingBox, filterList=[]):
    """
    This function requests data from openStreetMap
    @param boundingBox a list of the points of the boundingBox [minLat,minLon,maxLat,maxLon]
    @param filterList (optional) list of tripel of filter-rules e.g.(["way","node"],"amenity","univerity")
    @return an request object with the data-xml in the content property
    """
    return self._parseData(requests.get(self.osmurl,params=self._getOsmRequestData(boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3], filterList)),False)
  
  def _parseData(self, obj, isFile):
    """ """
    osmObj=osmData.OSM()
    
    if isFile:
      #needed, when working with xml file
      data = dom.parse(obj)
    else:
      data = dom.parseString(obj.content)
    
    for node in data.getElementsByTagName('node'):      
      node_id = int(node.getAttribute('id').encode('utf-8'))
      
      if (osmObj.nodes.has_key(node_id)):
        if len(osmObj.nodes[node_id].tags) == 0:
          osmObj.nodes[node_id].tags = self._getTags(node)
      else:
        node_tags = self._getTags(node)
        
        nodeObj=osmData.Node(node_id, float(node.getAttribute('lat')), float(node.getAttribute('lon')), node_tags)
        osmObj.addNode(nodeObj)
      
    for way in data.getElementsByTagName('way'):
      way_id = int(way.getAttribute('id').encode('utf-8'))
      
      if (osmObj.ways.has_key(way_id)):
        if len(osmObj.ways[way_id].refs) == 0:
          osmObj.ways[way_id].refs = self._getRefs(way)
        if len(osmObj.ways[way_id].tags) == 0:
          osmObj.ways[way_id].tags = self._getTags(way)
      
      else:
        if way.hasChildNodes():
          way_refs = self._getRefs(way)
          way_tags = self._getTags(way)
        
          wayObj = osmData.Way(way_id, way_refs, way_tags)  
          osmObj.addWay(wayObj)
      
    for relation in data.getElementsByTagName('relation'):
      rel_id = int(relation.getAttribute('id').encode('utf-8'))
      
      if (osmObj.relations.has_key(rel_id)):
        if len(osmObj.relations[rel_id].members) == 0:
          osmObj.relations[rel_id].refs = self._getMembers(relation)
        if len(osmObj.relations[rel_id].tags) == 0:
          osmObj.relations[rel_id].tags = self._getTags(relation)

      else:
        if relation.hasChildNodes() :
          rel_members = self._getMembers(relation)
          rel_tags = self._getTags(relation) 

          relObj = osmData.Relation(rel_id, rel_members, rel_tags)
          osmObj.addRelation(relObj)

    return osmObj

  def _getTags(self, node):
    tags = {}
    for element in node.getElementsByTagName('tag'):
        tags[element.getAttribute('k').encode('utf-8')] = element.getAttribute('v').encode('utf-8')
    
    return tags
  
  def _getRefs(self, node):
    refs = []
    for element in node.getElementsByTagName('nd'):
      refs.append(int(element.getAttribute('ref').encode( "utf-8" )))
      
    return refs

  def _getMembers(self, node):
    members = []
    for element in node.getElementsByTagName('member'):
      type = element.getAttribute('type').encode("utf-8")
      ref = int(element.getAttribute('ref').encode("utf-8"))
      role = element.getAttribute('role').encode("utf-8")
      members.append((type, ref, role))
      
    return members
