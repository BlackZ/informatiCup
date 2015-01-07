# coding=utf-8
"""
MapView
=======

.. author:: Mathieu Virbel <mat@kivy.org>

MapView is a Kivy widget that display maps.
"""

__all__ = ["Coordinate", "Bbox", "MapView", "MapSource", "MapMarker",
           "MapLayer", "MarkerMapLayer", "MapMarkerPopup"]
__version__ = "0.2"

MIN_LATITUDE = -90.
MAX_LATITUDE = 90.
MIN_LONGITUDE = -180.
MAX_LONGITUDE = 180.

try:
    import os
    import sys
    
    if "win32" == sys.platform:
        CACHE_DIR = os.path.expanduser('~') + "\AppData\Local\Temp\isySUR"
    elif "linux" in sys.platform or "darwin" == sys.platform or "os" in sys.platform:
        CACHE_DIR = '/tmp/isySUR'
    else:
        CACHE_DIR = 'cache'
        
    del os
    del sys
except Exception as e:
    print e

try:
    # fix if used within our programm
    import sys
    sys.modules['mapview'] = sys.modules['isySUR.gui.mapview']
    del sys
except KeyError:
    pass

from mapview.types import Coordinate, Bbox
from mapview.source import MapSource
from mapview.view import MapView, MapMarker, MapLayer, MarkerMapLayer, \
    MapMarkerPopup
