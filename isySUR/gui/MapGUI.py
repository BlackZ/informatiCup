#!/usr/bin/env python
#!/usr/bin/kivy

import os
from isySUR import kmlData

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from mapview import MapView

class Map(FloatLayout):
  
  def __init__(self, app):
    super(Map, self).__init__()
    
    self.app = app
    self.maps = MapView(zoom=11, lat=50.6394, lon=3.057)
    self.add_widget(self.maps, 20)
    
    self.menue = Menue(self)
    self.menue.auto_dismiss = False
    
    self.menue.setToast(self.ids.toast)
    
    self.kmlList = KMLList(self)
    self.kmlList.auto_dismiss = False
      
  def open_menue(self):
    if self.menue.isOpen:
      self.menue.dismiss(self.ids.menueBut)
    else:
      self.menue.open(self.ids.menueBut)
    self.menue.isOpen = not self.menue.isOpen
    
  def open_kmlList(self):
    if len(self.app.loaded_kmls) == 0:
      self.ids.toast.text = "No KML files loaded!"
    elif self.kmlList.is_open:
      self.kmlList.dismiss(self.ids.kml)
    else:
      self.kmlList.open(self.ids.kml)
    self.kmlList.is_open = not self.kmlList.is_open
  
class Menue(DropDown):
  loadfile = ObjectProperty(None)
  savefile = ObjectProperty(None)
  text_input = ObjectProperty(None)
  
  def __init__(self, app):
    super(Menue, self).__init__()
    self.text_input = TextInput()
    self.isOpen = False
    self.app = app
    self.toast = None
  
  def setToast(self, toast):
    self.toast = toast
  
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
      try:
        item_name = self.app.app.addKML(os.path.join(path, filename[0]))
      except:
        self.toast.text = "The loaded file is incomplete!"
      #with open(os.path.join(path, filename[0])) as stream:
      #    self.app.addKML(stream.read())
      self.app.kmlList.addItem(item_name)
  
    self.dismiss_popup()
  
  def save(self, path, filename):
    if filename != []:
      try:
        with open(os.path.join(path, filename), 'w') as stream:
          for kml in self.app.loaded_kmls:
            stream.write(kml.getXML())
      except:
        self.toast.text = "An error occured while saving!"

    self.dismiss_popup()

class KMLList(DropDown):
  def __init__(self, app):
    super(KMLList, self).__init__()
    
    self.app = app
    self.is_open = False
    self.createList()
  
  def createList(self):
    if len(self.app.app.loaded_kmls) != 0:
      for kml in self.app.loaded_kmls:
        btn = Button(text=self.app.loaded_kmls['name'], size_hint_y=None, height=44, background_color=(0,0,2,1))
        btn.bind(on_release=self.selectBut)
        self.add_widget(btn)
    
  def selectBut(self, obj):
    print obj.text
    selected = self.app.app.loaded_kmls[obj.text]['selected']
    if selected:
      obj.background_color = (0,0,2,1)
    else:
      obj.background_color = (1,1,1,1)
    self.app.app.loaded_kmls[obj.text]['selected'] = not selected

  def addItem(self, name):
    print name
    btn = Button(text=name, size_hint_y=None, height=44,background_color=(0,0,2,1))
    btn.bind(on_release=self.selectBut)
    self.add_widget(btn)
    
#class KMLList(BoxLayout):
#  def __init__(self, app, posi):
#    super(KMLList, self).__init__()
#    self.app = app
#    self.is_open = False
#    
#    list_item_args_converter = \
#          lambda row_index, rec: {'text':rec['name'],
#                                  'size_hint': (0.15, None)}
#    
#    kml_dict_adapter = \
#          DictAdapter(
#            sorted_keys=sorted(self.app.loaded_kmls.keys()),
#            data = self.app.loaded_kmls,
#            args_converter=list_item_args_converter,
#            selection_mode='multiple',
#            cls=ListItemButton)
#    
#    kml_view = ListView(adapter=kml_dict_adapter, size_hint=(0.2,1.0))
#    
#    self.add_widget(kml_view)
      
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
    
    self.loaded_kmls = {}
  
  def build(self):
    return Map(self)
  
  def addKML(self, kml):
    placemark = kmlData.KMLObject.parseKML(kml)
    name = "KML" + str(len(self.loaded_kmls) + 1)
    self.loaded_kmls.update({name:{'data':placemark, 'selected':False}})
    
    return name
    

if __name__ == '__main__':
  MapApp().run()  


