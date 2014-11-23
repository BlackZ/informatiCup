# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:47:29 2014

@author: jhemming & tschodde
"""

import unittest
import osmAPI
import osmData
import os
import xml.dom.minidom as dom

class TestOsmAPI(unittest.TestCase):
  def setUp(self):
    self.osmAPIobj=osmAPI.osmAPI()
    self.boundingBox = [52.032736,8.486593,52.042113,8.501194]
    self.osmDataFilename = "test.xml"

    self.testXMLString = "<relation id='152483'>"\
                         "<nd ref='43682400'/>"\
                         "<nd ref='260441217'/>"\
                         "<member type='way' ref='17958713' role='inner'/>"\
                         "<member type='way' ref='17958715' role='outer'/>"\
                         "<tag k='leisure' v='pitch'/>"\
                         "<tag k='type' v='multipolygon'/>"\
                         "</relation>"
    self.testNode = dom.parseString(self.testXMLString)
    
    self.testOsmObj = osmData.OSM()
    self.testOsmObj.addNode(osmData.Node("146891366", 52.0364239, 8.4867570,
                                         {"crossing":"traffic_signals","highway":"traffic_signals"}))
    self.testOsmObj.addNode(osmData.Node("46426098", 52.0375177, 8.4995645, {}))
    self.testOsmObj.addNode(osmData.Node("46426114", 52.0386730, 8.4981747, {}))
    self.testOsmObj.addWay(osmData.Way("46480681", ["593900008", "416938583"],
                                       {"bicycle":"yes","highway":"footway"}))
    self.testOsmObj.addRelation(osmData.Relation("152923",
                                                 [("way","35221623","outer")],
                                                 {"natural":"scrub","type":"multipolygon"}))
    self.testOsmObj.addRelation(osmData.Relation("905522",
                                                 [("way","26582813","outer"),(
                                                  "way","20213971","inner")],{"type":"multipolygon"}))
  
  def test_getOsmRequestData(self):
    testObj=self.osmAPIobj._getOsmRequestData(self.boundingBox[0],
                                              self.boundingBox[1],
                                              self.boundingBox[2],
                                              self.boundingBox[3],
                                              [])
    self.assertIsNotNone(testObj)
    self.assertEqual(testObj.has_key('data'),True)
    self.assertEqual(testObj['data'],'[out:xml][timeout:25];'\
                     '(node[""=""](52.032736,8.486593,52.042113,8.501194);'\
                     'way[""=""](52.032736,8.486593,52.042113,8.501194);'\
                     'relation[""=""](52.032736,8.486593,52.042113,8.501194););out body;>;out skel qt;')
    
    testObj2 = self.osmAPIobj._getOsmRequestData(self.boundingBox[0],
                                                 self.boundingBox[1],
                                                 self.boundingBox[2],
                                                 self.boundingBox[3],
                                                 filterList=[(["node","way","relation"],
                                                  "amenity","university")])
    self.assertIsNotNone(testObj2)
    self.assertEqual(testObj2.has_key('data'),True)
    self.assertEqual(testObj2['data'],'[out:xml][timeout:25];'\
                     '(node["amenity"="university"](52.032736,8.486593,52.042113,8.501194);'\
                     'way["amenity"="university"](52.032736,8.486593,52.042113,8.501194);'\
                     'relation["amenity"="university"](52.032736,8.486593,52.042113,8.501194););'\
                     'out body;>;out skel qt;')
   
  #def test_performRequest(self):
    #self.requestData = self.osmAPIobj.performRequest(self.boundingBox)
    #self.assertIsNotNone(self.requestData)
  
  def test_parseData(self):
    
    testFile = open(self.osmDataFilename, "r").read()
    
    testDataObj = self.osmAPIobj._parseData(testFile)
    
    self.assertIsNotNone(testDataObj)
    self.assertIsNotNone(testDataObj.nodes)
    self.assertIsNotNone(testDataObj.ways)
    self.assertIsNotNone(testDataObj.relations)    

    #self.assertTrue(self.testOsmObj == testDataObj)
    self.assertEqual(self.testOsmObj, testDataObj)
   
  def test_getTags(self):
    tags = {"leisure":"pitch", "type":"multipolygon"}
    
    testTags = self.osmAPIobj._getTags(self.testNode)
    
    self.assertIsNotNone(testTags)
    self.assertEqual(tags, testTags)
  
  def test_getRefs(self):
    refs = ["43682400","260441217"]
    
    testRefs = self.osmAPIobj._getRefs(self.testNode)
    
    self.assertIsNotNone(testRefs)
    self.assertEqual(refs, testRefs)
  
  def test_getMembers(self):
    members = [("way", "17958713","inner"),("way","17958715", "outer")]
    
    testMembers = self.osmAPIobj._getMembers(self.testNode)
    
    self.assertIsNotNone(testMembers)
    self.assertEqual(members, testMembers)
    
  #def test_parseData(self):
  #  testObj=self.osmAPIobj.performRequest(self.boundingBox)
  #  self.assertIsNotNone(testObj)
  #  self.assertIsNotNone(testObj.nodes)
  #  self.assertIsNotNone(testObj.ways)
  #  self.assertIsNotNone(testObj.relations)
  #  
  #  #test Nodes
  #  node_id = "2689012941"
  #  node_lon = "8.4997598"
  #  node_lat = "52.0338123"
  #  self.assertTrue(node_id in testObj.nodes)
  #  self.assertEqual(testObj.nodes[node_id].lat, node_lat)
  #  self.assertEqual(testObj.nodes[node_id].lon, node_lon)
  #  self.assertIsNotNone(testObj.nodes[node_id].tags)
  #  
  #  #test Ways
  #  way_id = "58717810"
  #  way_refs_len = 5
  #  way_tags_len = 6
  #  way_name = {} #Why is this here if it is not used?
  #  self.assertTrue(way_id in testObj.ways)
  #  self.assertEqual(len(testObj.ways[way_id].refs), way_refs_len)
  #  self.assertEqual(len(testObj.ways[way_id].tags), way_tags_len)
  #  
  #  #test Relations
  #  rel_id = "3454079"
  #  rel_members_len = 1
  #  rel_tags_len = 3
  #  rel_tag_key = "name"
  #  rel_tag_value = "Spannungsbogen"
  #  self.assertTrue(rel_id in testObj.relations)
  #  self.assertEqual(len(testObj.relations[rel_id].members), rel_members_len)
  #  self.assertEqual(len(testObj.relations[rel_id].tags), rel_tags_len)
  #  self.assertTrue(rel_tag_key in testObj.relations[rel_id].tags)
  #  self.assertEqual(rel_tag_value, testObj.relations[rel_id].tags[rel_tag_key])


if __name__ == '__main__':
  os.chdir("..")
  unittest.main()