#!/usr/bin/env python
#!/usr/bin/kivy

import os
import sys
#sys.path.append("..")
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import kmlData

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.listview import ListView
from kivy.uix.dropdown import DropDown
from kivy.factory import Factory
from gui.sidepanel import SidePanel
from gui.MapViewer import MapViewer
import gui.WMSTileServer
from gui.WMSOverlayServer import *

class Map(FloatLayout):
    def __init__(self, app):
        super(Map, self).__init__()
        self.maps = MapViewer(maptype="Roadmap", provider="openstreetmap")
        self.add_widget(self.maps, 20)
        
        self.menue = Menue(app)
        self.menue.auto_dismiss = False
        
    def open_menue(self):
        if self.menue.isOpen:
            self.menue.dismiss(self.ids.menueBut)
        else:
            self.menue.open(self.ids.menueBut)
        self.menue.isOpen = not self.menue.isOpen
    
class Menue(DropDown):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def __init__(self, app):
        super(Menue, self).__init__()
        self.text_input = TextInput()
        self.isOpen = False
        self.app = app
    
    def dismiss_popup(self):
        self._popup.dismiss()
    
    def show_load(self):
        self.isOpen = not self.isOpen
        self.dismiss()
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def show_save(self):
        self.isOpen = not self.isOpen
        self.dismiss()
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def load(self, path, filename):
        if filename != []:
            self.app.addKML(os.path.join(path, filename[0]))
            #with open(os.path.join(path, filename[0])) as stream:
            #    self.app.addKML(stream.read())
    
            self.dismiss_popup()
    
    def save(self, path, filename):
        if filename != []:
            with open(os.path.join(path, filename), 'w') as stream:
                for kml in self.app.loaded_kmls:
                    stream.write(kml.getXML())

        self.dismiss_popup()

#class KMLList(ListView):
    #def __init__(self, app):
    #    super(KMLList, self).__init__()
    #    self.app = app
        
    #def createData(self):
    #    check_list = []
    #    for kml in self.app.loaded_kmls:
    #        checkList.append(CheckBox())
    

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    filters = ["*.kml"]

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
class MapApp(App):
    
    def __init__(self):
        super(MapApp, self).__init__()
        
        self.loaded_kmls = []
    
    def build(self):
        return Map(self)
    
    def addKML(self, kml):
        placemark = kmlData.KMLObject.parseKML(kml)
        self.loaded_kmls.append(placemark)
        
        print placemark

#if __name__ == '__main__':
#    MapApp().run()
    


