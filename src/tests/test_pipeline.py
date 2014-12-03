# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:53:07 2014

@author: jhemming
"""

import unittest
import programm

class TestProgrammPipeline(unittest.TestCase):
    
    def setUp(self):
        self.kmlObject = None
    
    def test_pipeline(self):
        pipeObj = programm.Pipeline()
        kml = pipeObj.pipeline()
        self.fail("TODO implement")
        

