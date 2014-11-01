# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:31:51 2014
Basic class to load and store space usage rules.
@author: jpoeppel

Current Problems:
*Shouldn't ruleName be a list since several rules can apply to the same id?
*should the ruleName not be split into type and "option" since we have things like smoking=no or access:age="21+"?
"""

class SUR():
  
  def __init__(self, surID, name, lat, lon):
    self.id = surID
    self.ruleName = name
    self.longitude = lon
    self.latitude = lat
  
  @classmethod
  def fromString(cls, s):
    data = s.replace(" ", "").split(',')
    return cls(data[0], data[3], float(data[1]), float(data[2]))
