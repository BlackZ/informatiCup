# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 14:58:31 2014

@author: adreyer & jpoeppel
"""

import unittest

if __name__ == '__main__':
  testLoader = unittest.TestLoader()
  suite = testLoader.discover('.')
  unittest.TextTestRunner(verbosity=2).run(suite)