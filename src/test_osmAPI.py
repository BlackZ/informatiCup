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
    
  def test_getOsmRequestData(self, ):
    boundingBox=[52.032736,8.486593,52.042113,8.501194]
    testObj=self.osmAPIobj.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])
    self.assertIsNotNone(testObj)
    self.assertEqual(testObj.has_key('data'),True)
    self.assertEqual(testObj['data'],'[out:xml][timeout:25];(node[""=""](52.032736,8.486593,52.042113,8.501194);way[""=""](52.032736,8.486593,52.042113,8.501194);relation[""=""](52.032736,8.486593,52.042113,8.501194););out body;>;out skel qt;')
    
  def test_performRequest(self):
    boundingBox=[52.032736,8.486593,52.042113,8.501194]
    testObj=self.osmAPIobj.performRequest(boundingBox)
    self.assertIsNotNone(testObj)

  
