# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:47:29 2014

@author: jpoeppel
"""

import unittest
import osmAPI

class TestOsmAPI(unittest.TestCase):
  def setUp(self):
    self.osmAPIobj=osmAPI.osmAPI()
    self.boundingBox = [52.032736,8.486593,52.042113,8.501194]
    
  def test_getOsmRequestData(self, ):
    testObj=self.osmAPIobj.getOsmRequestData(self.boundingBox[0],self.boundingBox[1],self.boundingBox[2],self.boundingBox[3])
    self.assertIsNotNone(testObj)
    self.assertEqual(testObj.has_key('data'),True)
    self.assertEqual(testObj['data'],'[out:xml][timeout:25];(node[""=""](52.032736,8.486593,52.042113,8.501194);way[""=""](52.032736,8.486593,52.042113,8.501194);relation[""=""](52.032736,8.486593,52.042113,8.501194););out body;>;out skel qt;')
 
#This does nothing the next test doesn't do.   
#  def test_performRequest(self):
#    testObj=self.osmAPIobj.performRequest(self.boundingBox)
#    self.assertIsNotNone(testObj)
    
  def test_parseData(self):
    testObj=self.osmAPIobj.performRequest(self.boundingBox)
    self.assertIsNotNone(testObj)
    self.assertIsNotNone(testObj.nodes)
    self.assertIsNotNone(testObj.ways)
    self.assertIsNotNone(testObj.relations)
    
    #test Nodes
    node_id = "2689012941"
    node_lon = "8.4997598"
    node_lat = "52.0338123"
    self.assertTrue(node_id in testObj.nodes)
    self.assertEqual(testObj.nodes[node_id].lat, node_lat)
    self.assertEqual(testObj.nodes[node_id].lon, node_lon)
    self.assertIsNotNone(testObj.nodes[node_id].tags)
    
    #test Ways
    way_id = "58717810"
    way_refs_len = 5
    way_tags_len = 6
    way_name = {} #Why is this here if it is not used?
    self.assertTrue(way_id in testObj.ways)
    self.assertEqual(len(testObj.ways[way_id].refs), way_refs_len)
    self.assertEqual(len(testObj.ways[way_id].tags), way_tags_len)
    
    #test Relations
    rel_id = "3454079"
    rel_members_len = 1
    rel_tags_len = 3
    rel_tag_key = "name"
    rel_tag_value = "Spannungsbogen"
    self.assertTrue(rel_id in testObj.relations)
    self.assertEqual(len(testObj.relations[rel_id].members), rel_members_len)
    self.assertEqual(len(testObj.relations[rel_id].tags), rel_tags_len)
    self.assertTrue(rel_tag_key in testObj.relations[rel_id].tags)
    self.assertEqual(rel_tag_value, testObj.relations[rel_id].tags[rel_tag_key])

  
