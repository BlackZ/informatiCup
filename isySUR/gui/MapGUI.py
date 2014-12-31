#!/usr/bin/env python

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from sidepanel import SidePanel
from MapViewer import MapViewer
import WMSTileServer
from WMSOverlayServer import *

class Map(FloatLayout):
    def __init__(self):
        super(Map, self).__init__()
        self.maps = MapViewer(maptype="Roadmap", provider="openstreetmap")
        self.add_widget(self.maps, 20)
        
    def merry_christmas(self):
        self.ids.toast.text = "Frohe Weihnachten!"
    
    def happy(self):
        self.ids.toast.text = "Guten Rutsch!"

class MapApp(App):
    def build(self):
        return Map()


if __name__ == '__main__':
    MapApp().run()