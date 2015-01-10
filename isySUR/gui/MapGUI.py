#!/usr/bin/env python
#!/usr/bin/kivy
from kivy.config import Config
Config.set('graphics','resizable',0)


import os
from signal import signal, SIGINT
from threading import Thread,Lock
from Queue import Queue

from isySUR import kmlData, program
from mapview import MapView

from kivy import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
                          ListProperty
                          

class Map(FloatLayout):
  
  text = StringProperty()
  
  def __init__(self, app):
    super(Map, self).__init__()
    
    self.lock = Lock()
    self.app = app
    self.maps = MapView(zoom=11, lat=50.6394, lon=3.057)
    self.maps.center_on(52.023368, 8.538291)
    self.add_widget(self.maps, 20)
    self.toastLabel = Label(bold=True, font_size=20, color=(1,1,1,1))
    
    self.kmlList = KMLList(self, app)
    self.menue = Menue(self, app)
  
  def cleanUpCache(self):
    """
    Triggers function to delete cache folder.
    """
    self.maps.cleanUpCache()
  
  def toast(self, text, long_duration=False):
    """
    Shows a toast.
    
    @param duration: If paramter is True the toast is
                     visible for a long time. Otherwise
                     it has a shorter duration.
    @type duration: Boolean
    """
    Toast(self).show(text, long_duration)
      
  def open_menue(self):
    """
    Opens and closes the Main Menu.
    """
    if self.menue.isOpen:
      self.menue.dismiss(self.ids.menueBut)
    else:
      self.menue.open(self.ids.menueBut)
    self.menue.isOpen = not self.menue.isOpen
    
  def open_kmlList(self):
    """
    Opens and closes the KML List.
    """
    if len(self.app.loaded_kmls) == 0:
      self.toast("No KML files loaded!")
    elif self.kmlList.is_open:
      self.kmlList.dismiss(self.ids.kmlList)
      self.kmlList.is_open = not self.kmlList.is_open  
    else:
      self.kmlList.open(self.ids.kmlList)
      self.kmlList.is_open = not self.kmlList.is_open      
  
  #def addPolygon(self, polygon, first=True):
  #  name, poly = polygon
  #  style = self.app.loaded_kmls[name]['style']
  #  markerCoords = self.app.loaded_kmls[name]['data'].ruleCoords
  #  self.maps.addPolygon(name, poly, style, markerCoords)
  #  
  #  if first:
  #    self.maps.zoom_to_Polygon(name, 15)
  #  return name
  
  def showPolygons(self, names):
    for name in names:
      move_to = name
      self.maps.showPolygon(name)
    self.maps.zoom_to_Polygon(move_to, 15)
  
  def hidePolygons(self, names):
    for name in names:
      self.maps.hidePolygon(name)
   
  def addPolygon(self, kmlObj, kmlName, first=True):
    print kmlObj.placemarks
    for placemark in kmlObj.placemarks:
      print placemark
      name = placemark.name
      print "bla"
      polygon = self.app.getPolygonFromPlacemark(placemark)
      print "blu"
      style = kmlObj.styles[placemark.style.lstrip('#')]
      print 'bloe'
      i = 1
      print self.maps.placemarks.has_key(name)
      while self.maps.placemarks.has_key(name):
        print name
        name = placemark.name + '(' + str(i) + ')'
        i += 1
      
      self.maps.addPolygon(name, polygon, style, placemark.ruleCoords)
      self.app.loaded_kmls[kmlName]['polygons'].append(name)
      
      moved = False
      if len(kmlObj.placemarks) == 1 and first:
        moved = True
        self.maps.zoom_to_Polygon(name, 15)
    return name, moved
  
  #def addPolygon(self, kmlObj, name, first=True):
  #  """
  #  Adds all polygons from one KML.
  #  
  #  @param kmlObj: KML obect which will be added to map
  #  @type kmlObj: kmlData.KMLObject
  #  
  #  @param first: Decides whether the map zooms to the
  #                first or last added polygon.
  #  @type first: Bool
  #  
  #  @return: Returns the coordinates to which will be moved.
  #           Only relevant for move to the last added. 
  #  """
  #  placemarks = kmlObj.placemarks
  #  for placemark in placemarks:
  #    style = kmlObj.styles[placemark.style.lstrip('#')]
  #    self.maps.addPolygon(name, self.app.getPolygonFromPlacemark(placemark), style, placemark.ruleCoords)
  #    #moves to added Polygon
  #    if first:
  #      self.maps.zoom_to_Polygon(name, 15)
  #       
  #  return name
    
    
  def removePolygon(self, name):#polygon):
    self.maps.removePolygon(name)
  
  def computeAndShowKmls(self, path, queue):
    toast = Toast(self)
    toast.stayVisible("Calculating ... ")
    #self.toastLabel.text = "Calculating ..."
    #self.toastLabel.texture_update()
    #self.toastLabel.pos=(0, -self.center_y + self.toastLabel.texture_size[1]/2 + 10)
    kmlList = Queue()
    #self.add_widget(self.toastLabel)
    #with self.toastLabel.canvas.before:
    #  Color(0.6,0.6,0.6,1)#self._transparency)
    #  Rectangle(pos=(self.center_x - self.toastLabel.texture_size[0] -10, 6), 
    #            size=(self.toastLabel.texture_size[0]*2+14, self.toastLabel.texture_size[1]+ 10))
    #  Color(0.2,0.2,0.2,1)#self._transparency)
    #  Rectangle(pos=(self.center_x - self.toastLabel.texture_size[0] -8, 8), 
    #            size=(self.toastLabel.texture_size[0]*2+10, self.toastLabel.texture_size[1]+ 6))
    
    thread = Thread(target=self.app.pipe._computeKMLs, args=(path, kmlList))
    thread.daemon=True
    thread.start()
    
    surID = "" # Ueberfluessig, wenn Name in KML!!!
    while not kmlList.empty() or thread.isAlive():
      item = kmlList.get()
      if isinstance(item, kmlData.KMLObject):
        if not item.placemarks == []:
          self.lock.acquire()
          #name = self.app.addKML(surID, item)
          name = self.app.addKML(item)
          self.kmlList.addItem(name)
          self.lock.release()
          move_to, moved = self.addPolygon(item, name, first=False)
          #name = self.addPolygon(item, name, first=False)
          #polygons = self.app.addKML(item)
          #for polygon in polygons:
          #  self.kmlList.addItem(polygon[0])
          #  move_to = self.addPolygon(polygon, first=False)
          #self.lock.release()
      else:
        toast.stayVisible("Calculating " + item + " ...")
        #self.toastLabel.text = "Calculating " + item + " ..."
        #self.toastLabel.texture_update()
    
    if not moved:
      self.maps.zoom_to_Polygon(move_to, 15)
    toast.remove()
    #self.remove_widget(toast)
    #Clock.schedule_interval(self._in_out, 1/60.0)
  
  #def _in_out(self, dt):
  #  duration -= dt*1000
  #  if self._duration <= 0:
  #    self._transparency = 1.0 + (self._duration / self._rampdown)
  #  if -(self._duration) > self._rampdown:
  #    self.map_view.remove_widget(self)
  #    return False
  
    
    
    
class Menue(DropDown):
  loadfile = ObjectProperty(None)
  savefile = ObjectProperty(None)
  text_input = ObjectProperty(None)
  
  def __init__(self, mapview, app):
    super(Menue, self).__init__()
    self.text_input = TextInput()
    self.isOpen = False
    self.auto_dismiss = False

    if "win" == platform or "linux" == platform or "macosx" == platform:
      self.path = '.'
    else:
      self.path = '/'

    self.map_view =mapview
    self.app = app

    self.config = None
    
    self.queue = Queue()
    self._SURThread=None
  
  def dismiss_load(self):
    self._popup_load.dismiss()
  
  def dismiss_save(self):
   self._popup_save.dismiss()
  
  def dismiss_config(self):
   self._popup_config.dismiss()
   self.config = None
  
  def show_load(self, obj, config=None):
    self.isOpen = False
    self.dismiss()
    content = LoadDialog(load=self.load, cancel=self.dismiss_load)
    content.ids.filechooser.path = self.path
    if 'KML' in obj.text:
      content.ids.filechooser.filters = ['*.kml']
    elif 'SUR' in obj.text:
      if self._SURThread == None or (self._SURThread != None and not self._SURThread.isAlive()):
        content.ids.filechooser.filters = ['*.txt']
      elif self._SURThread != None or self._SURThread.isAlive():
          self.map_view.toast('Already calculating!')
          return      
    else:
      content.ids.filechooser.filters = ['*.cfg']
    self._popup_load = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
    self._popup_load.open()
  
  def show_save(self, isConfig=False):
    self.isOpen = False
    self.dismiss()
    if isConfig:
      content = SaveDialog(save=self.saveConfig, cancel=self.dismiss_save)
    else:
      content = SaveDialog(save=self.saveKML, cancel=self.dismiss_save)
    selection = self.app.getSelectedPolygons()
    if len(selection) > 0:
      content.ids.filechooser.path = self.path
      self._popup_save = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
      self._popup_save.open()
    else:
      self.map_view.toast("No KML files selected or loaded!")
    
      
  def show_config(self):
    self.isOpen = False
    self.dismiss()
    
    self.config = ConfigDialog(self.app, save=self.show_save, load=self.show_load, cancel=self.dismiss_config)
    self._popup_config = Popup(title="Configurate SUR-Rules", content=self.config, size_hint=(0.9, 0.9))

    self._popup_config.open()
  
  def load(self, path, filename, config=None):    
    if filename != []:
      #path = os.path.join(path, filename[0])
      path = filename[0]
      name, ext = os.path.splitext(filename[0])
      name = (name.replace('\\','/').split('/'))[-1]
      if ext == '.kml':
        try:
          kmlObj = kmlData.KMLObject.parseKML(path)
          name = self.app.addKML(kmlObj)
          
          self.map_view.kmlList.addItem(name)
          name, moved = self.map_view.addPolygon(kmlObj, name)
          if not moved:
            self.map_view.maps.zoom_to_Polygon(name, 15)
          
          #polygons = self.app.addKML(kmlObj)
          
          #for polygon in polygons:
          #  self.map_view.kmlList.addItem(polygon[0])
          #  self.map_view.addPolygon(polygon)
          
          #item_name, kmlObj = self.app.addKMLFromPath(path, name)
          #if not kmlObj.placemarks==[]:
          #  self.map_view.kmlList.addItem(item_name)
          #  self.map_view.addPolygon(kmlObj, item_name)
          #else:
          #  self.map_view.toast('The loaded KML has no polygon!')
        except Exception as e:
          print e
          import traceback
          traceback.print_exc()
          self.map_view.toast('The loaded KML file is incomplete!')
          #add new kml to dropdown menue
      
      if ext == '.cfg':
        self.app.loadConfig(path)
        
        if len(self.app.configContent) > 0:
          self.config.addConfigContent()
          
      self.dismiss_load()
      
      if ext == '.txt':
        if self._SURThread==None or not self._SURThread.isAlive():
          self._SURThread=Thread(target=self.map_view.computeAndShowKmls, args=(path, self.queue, ))
          self._SURThread.daemon=True
          self._SURThread.start()
          
  def saveConfig(self, path, filename):
    if filename != "":
    
      config = {'[Indoor]':[], '[Outdoor]':[], '[Both]':[]}
    
      for layout in self.config.ids.view.children:
        if isinstance(layout, GridLayout):
          i = 0
          while i < (len(layout.children) - 5)/5:
    
            children = layout.children[(5*i):(5*(i+1))]
            rule = ""
            key = ""
            for elem in children:
              if isinstance(elem, Label):
                rule = elem.text
              if isinstance(elem, CheckBox):
                if elem.active:
                  key = elem.id
            config[key].append(rule)
            i += 1
      name, ext = os.path.splitext(filename)
      if ext == '':
        filename = filename + '.cfg'
      with open(os.path.join(path, filename), 'w') as stream:
        for ruleArea in config:
          stream.write(ruleArea + '\n')
          for rule in config[ruleArea]:
            stream.write(rule + '\n')
      
      self.dismiss_save()
  
  def saveKML(self, path, filename):
    isDir = os.path.isdir(os.path.join(path, filename))
    completeKML = kmlData.KMLObject("complete")
    
    selection = self.app.getSelectedPolygons()
    if len(selection) > 0:
      for elem in selection:         
        if isDir:  
          try:
            selection[elem].saveAsXML(path + os.path.sep + elem + '.kml')
          except:
            import traceback
            traceback.print_exc()
            self.map_view.toast(elem + " could not be saved!")
        print selection[elem].placemarks
        completeKML.placemarks.extend(selection[elem].placemarks)
        completeKML.addStyles(selection[elem].styles)
      if len(completeKML.placemarks) > 0:
        try:
          if isDir:
            completeKML.saveAsXML(path + os.path.sep + 'complete.kml')
          else:
            name, ext = os.path.splitext(filename)
            if ext == '':
              filename = filename + '.kml'
            with open(os.path.join(path, filename), 'w') as stream:
              stream.write(completeKML.getXML())
        except Exception as e:
          print e
          import traceback
          traceback.print_exc()
          self.map_view.toast('An error occured while saving!')
          #map_view.ids.toast.text = "An error occured while saving!"
    else:
      self.map_view.toast("No KML files selected or loaded!")

    self.dismiss_save()
  
  def switchMarkers(self, obj):
    if self.map_view.maps.markers:
      obj.background_color = (1,1,1,1)
      self.map_view.maps.markers = False
      self.map_view.maps.hideMarkers()
    elif not self.map_view.maps.markers:
      obj.background_color = (0,0,2,1)
      self.map_view.maps.markers = True
      self.map_view.maps.showMarkers()
    
#    if "Hide" in obj.text:
#      obj.text = "Show Markers"
#      self.map_view.maps.markers = False
#      self.map_view.maps.hideMarkers()
#    elif "Show" in obj.text:
#      obj.text = "Hide Markers"
#      self.map_view.maps.markers = True
#      self.map_view.maps.showMarkers()


class CustomFileChooser(FileChooserListView):
  """
    Implemented this and override the following method to fix path bug.
  """
 
  def open_entry(self, entry):
        newPath = ''
        entry_path = entry.path.replace('\\', '/')
        if entry_path == '../':
          newPath = os.path.join(self.path, entry_path[:-1])
        else:
          tmp = entry_path.split('/')
          newPath = os.path.join(self.path, tmp[-1])
        
        if os.path.isdir(newPath):
          self.path = newPath 
          self.selection = []


class KMLList(DropDown):
  def __init__(self, mapview, app):
    super(KMLList, self).__init__()
    self.map_view = mapview
    self.app = app
    self.is_open = False
    self.createList()
    self.auto_dismiss = False
  
  def createList(self):
    if len(self.app.loaded_kmls) != 0:
      for kml in self.app.loaded_kmls:
        btn = Button(text=self.app.loaded_kmls['name'], size_hint_y=None, height=44, background_color=(0,0,2,1))
        btn.bind(on_release=self.selectBut)
        self.add_widget(btn)
    
  def selectBut(self, obj):
    isSelected = self.app.loaded_kmls[obj.text]['selected']
    polygons = self.app.loaded_kmls[obj.text]['polygons']
    if not isSelected:
      obj.background_color = (0,0,2,1)
      self.map_view.showPolygons(polygons)
      #self.map_view.addPolygon((obj.text, self.app.getPolygonFromPlacemark(placemark)))
      self.app.loaded_kmls[obj.text]['selected'] = not isSelected
    else:
      if len(polygons) == 1 and self.map_view.maps.isPolyVisible(polygons[0]) or\
         len(polygons) > 1 and self.map_view.maps.isPolyVisible(polygons[-1]):
        obj.background_color = (1,1,1,1)
        #for placemark in placemarks:
  #        self.map_view.removePolygon(self.app.getPolygonFromPlacemark(placemark))
        self.map_view.hidePolygons(polygons)
        #self.map_view.removePolygon(obj.text)
        self.app.loaded_kmls[obj.text]['selected'] = not isSelected
      else:
        self.map_view.showPolygons(polygons)
        #self.map_view.addPolygon((obj.text, self.app.getPolygonFromPlacemark(placemark)))

  def addItem(self, name):
    btn = Button(text=name, size_hint_y=None, height=44,background_color=(0,0,2,1))
    btn.bind(on_release=self.selectBut)
    self.add_widget(btn)

class Toast(Label):
  _transparency = NumericProperty(1.0)
  _background = ListProperty((0, 0, 0, 1))
  
  def __init__(self, mapview):
    super(Toast, self).__init__()
    self.map_view = mapview
    print self.texture_size, self.text_size
  
  def stayVisible(self, text):
    self.text = text
    self.texture_update()
    
    self.pos=(0, -self.map_view.center_y + self.texture_size[1]/2 + 10)
    if self.parent != self.map_view:
      self.map_view.add_widget(self)
    with self.canvas.before:
      Color(0.6,0.6,0.6,1)#self._transparency)
      Rectangle(pos=(self.map_view.center_x - self.texture_size[0] -10, 6), 
                size=(self.texture_size[0]*2+14, self.texture_size[1]+ 10))
      Color(0.2,0.2,0.2,1)#self._transparency)
      Rectangle(pos=(self.map_view.center_x - self.texture_size[0] -8, 8), 
                size=(self.texture_size[0]*2+10, self.texture_size[1]+ 6))
    
  def remove(self):
    self._duration = 100
    self._rampdown = 100
  
    Clock.schedule_interval(self._in_out, 1/60.0)

  def show(self, text, length_long):
    duration = 5000 if length_long else 1000
    rampdown = duration * 0.1
    if rampdown > 500:
      rampdown = 500
    if rampdown < 100:
      rampdown = 100
    
    self._rampdown = rampdown
    self._duration = duration - rampdown
    self.text = text
    self.texture_update()
    self.pos=(0, -self.map_view.center_y + self.texture_size[1]/2 + 10)
    self.map_view.add_widget(self)
    with self.canvas.before:
      Color(0.6,0.6,0.6,1)#self._transparency)
      Rectangle(pos=(self.map_view.center_x - self.texture_size[0] -10, 6), 
                size=(self.texture_size[0]*2+14, self.texture_size[1]+ 10))
      Color(0.2,0.2,0.2,1)#self._transparency)
      Rectangle(pos=(self.map_view.center_x - self.texture_size[0] -8, 8), 
                size=(self.texture_size[0]*2+10, self.texture_size[1]+ 6))
  
    Clock.schedule_interval(self._in_out, 1/60.0)
  
  def _in_out(self, dt):
    self._duration -= dt*1000
    if self._duration <= 0:
      self._transparency = 1.0 + (self._duration / self._rampdown)
    if -(self._duration) > self._rampdown:
      self.map_view.remove_widget(self)
      return False
  
class LoadDialog(FloatLayout):
  load = ObjectProperty(None)
  cancel = ObjectProperty(None)
  test = ObjectProperty(None)

class SaveDialog(FloatLayout):
  save = ObjectProperty(None)
  text_input = ObjectProperty(None)
  cancel = ObjectProperty(None)
  
class ConfigDialog(FloatLayout):
  
  def __init__(self, app, save, load, cancel):
    super(ConfigDialog, self).__init__()
    self.auto_dismiss = False

    self.app = app    
    
    self.load = load
    self.save = save
    self.cancel = cancel
    
    self.info = Label(text="No configuration file loaded!")
    self.counter = 1
    self.layout = GridLayout(cols=5, size_hint_y=1.1)
    
    self.selected = []
    self.ruleInput = TextInput(focus=True, size_hint=(.4,.15))
    self.labels = []
    if len(self.app.configContent) > 0:
      self.addConfigContent()
    else:
      self.layout.add_widget(self.info)
    self.ids.view.add_widget(self.layout)
    
  def addConfigContent(self):
    if self.info.parent != None:
      self.layout.remove_widget(self.info)
    if len(self.layout.children) > 1:
      self.layout.clear_widgets()
    self.addContentHeader()
    
    for ruleArea in self.app.configContent:
      for rule in self.app.configContent[ruleArea]:
        self.addConfigEntry(ruleArea, rule)
  
  def addContentHeader(self):
    label1 = Label(text='', size_hint=(.4,.1))      
    label2 = Label(text='Indoor', size_hint=(.1,.1))
    label3 = Label(text='Outdoor', size_hint=(.1,.1))
    label4 = Label(text='Both', size_hint=(.1,.1))
    label5 = Label(text='Delete', size_hint=(.1,.1))
    
    
    self.layout.add_widget(label1)
    self.layout.add_widget(label2)
    self.layout.add_widget(label3)
    self.layout.add_widget(label4)
    self.layout.add_widget(label5)
  
  def addConfigEntry(self, ruleArea, rule):
    active={"[Indoor]":False,"[Outdoor]":False,"[Both]":False}
    active[ruleArea] = True
    
    group = str(self.counter)
    label = Label(text=rule, size_hint=(.4,.1))
    self.labels.append(label)
    btn1 = CheckBox(group=group, active=active['[Indoor]'], size_hint=(.1,.1), id='[Indoor]')
    btn2 = CheckBox(group=group, active=active['[Outdoor]'], size_hint=(.1,.1), id='[Outdoor]')
    btn3 = CheckBox(group=group, active=active['[Both]'], size_hint=(.1,.1), id='[Both]')
    btn4 = CheckBox(size_hint=(.1, .1), id=group, active=False)
    
    btn1.bind(active=self.changeRuleArea)
    btn2.bind(active=self.changeRuleArea)
    btn3.bind(active=self.changeRuleArea)
    btn4.bind(active=self.deleteEntry)
    
    self.layout.add_widget(label)
    self.layout.add_widget(btn1)
    self.layout.add_widget(btn2)
    self.layout.add_widget(btn3)
    self.layout.add_widget(btn4)
    
    self.counter += 1
  
  def changeRuleArea(self, *args):
    for value in args:
      if isinstance(value, CheckBox):
        group = value.group
        rule = self.labels[int(group) - 1].text
        if value.active:    
          self.app.configContent[value.id].append(rule)
        else:
          oldArea = self.app.configContent[value.id]
          if rule in oldArea:
            oldArea.remove(rule)    
    
  def action(self, obj):
    #if len(self.app.configContent) > 0:
    if "New" in obj.text:
      if len(self.app.configContent)==0:
        self.addConfigContent()
      obj.text = "Add Rule"
      self.ruleInput.text = ""
      self.layout.add_widget(self.ruleInput)
      self.ids.view.scroll_y = 0 
    elif "Add" in obj.text:
      obj.text = "New Rule"
      self.layout.remove_widget(self.ruleInput)
      if self.ruleInput.text != "":
        if len(self.app.configContent.keys())==0:
          self.app.configContent = {'[Both]':[],'[Indoor]':[],'[Outdoor]':[]}
        self.app.configContent['[Both]'].append(self.ruleInput.text)
        
        group = str(self.counter)
        label = Label(text=self.ruleInput.text, size_hint=(.4,.1))
        self.labels.append(label)
        btn1 = CheckBox(group=group, active=False, size_hint=(.1,.1), id='[Indoor]')
        btn2 = CheckBox(group=group, active=False, size_hint=(.1,.1), id='[Outdoor]')
        btn3 = CheckBox(group=group, active=True, size_hint=(.1,.1), id='[Both]')
        btn4 = CheckBox(size_hint=(.1, .1), id=group, active=False)
        
        btn1.bind(active=self.changeRuleArea)
        btn2.bind(active=self.changeRuleArea)
        btn3.bind(active=self.changeRuleArea)
        btn4.bind(active=self.deleteEntry)
        
        self.layout.add_widget(label)
        self.layout.add_widget(btn1)
        self.layout.add_widget(btn2)
        self.layout.add_widget(btn3)
        self.layout.add_widget(btn4)
        
        self.counter += 1
        self.ids.view.scroll_y = 0
    elif 'Delete' in obj.text:
      remove = []
      print "Delete"
      obj.text = "New Rule"
      for selection in self.selected:
        label = self.labels[int(selection) -1]
        remove.append(label)
        rule = label.text
        for values in self.app.configContent.values():
          if rule in values:
            values.remove(rule)
        for child in self.layout.children:
          if isinstance(child, CheckBox) and \
           (child.id == selection or child.group == selection):
            remove.append(child)
      self.layout.clear_widgets(remove)
      if len([y for x in self.app.configContent.values() for y in x])==0:
        self.layout.clear_widgets()  
        self.layout.add_widget(self.info)
        
  def deleteEntry(self, *args):
    for value in args:
      if isinstance(value, CheckBox):
    
        if value.active:
          self.selected.append(value.id)
        else:
          if len(self.selected) > 0:
            self.selected.remove(value.id)
      
    if len(self.selected) > 1:
      self.ids.action.text="Delete selected Rules!"
    elif len(self.selected) == 1:
      self.ids.action.text="Delete selected Rule!"
    else:
      self.ids.action.text="New Rule"
  
class MapApp(App):
  
  def __init__(self, configPath=""):
    super(MapApp, self).__init__()
    self.map = None
    self.configContent = {}
    self.loadConfig(configPath)
    
    self.pipe = program.Pipeline()
    self.loaded_kmls = {}

  def on_stop(self):
    self.map.cleanUpCache()
  
  def on_start(self):
    signal(SIGINT, self.stop) #Captures ctrl-c to exit correctly
    self.icon = 'logo.png'
    self.title = 'isySUR'
    
  def build(self):
    self.map = Map(self)
    return self.map
  
  def loadConfig(self, configPath):
    if configPath != '':
      self.configContent = {'[Both]':[],'[Indoor]':[],'[Outdoor]':[]}
      with open(configPath, 'r') as stream:
        for line in stream:
          line = line.replace('\n','')
          if line.startswith('['):
            key = line
            if not key in self.configContent.keys():
              self.configContent.update({key:[]})
          else:
            self.configContent[key].append(line)
  
  #def addKML(self, kmlObj):
  #  addedPolygons = []
  #  for placemark in kmlObj.placemarks:
  #    name = placemark.name
  #    styleID = placemark.style.lstrip('#')
  #    
  #    i = 1
  #    while self.loaded_kmls.has_key(name):
  #      name = placemark.name + '(' + str(i) + ')'
  #      i += 1
  #    
  #    self.loaded_kmls.update({name:{'data':placemark,
  #                                   'style':kmlObj.styles[styleID],
  #                                   'selected': True}})
  #    addedPolygons.append((name, self.getPolygonFromPlacemark(placemark)))
  #  
  #  return addedPolygons
   
  def addKML(self, kmlObj):
    name = kmlObj.name
    i = 1
    while self.loaded_kmls.has_key(name):
      name = kmlObj.name + '(' + str(i) + ')'
      i += 1
    
    self.loaded_kmls.update({name:{'data':kmlObj,'polygons':[],'selected':True}})
    
    return name
          
  #def addKML(self, name, kmlObj):
  #  newName = name
  #  i = 1
  #  while self.loaded_kmls.has_key(newName):
  #    newName = name + '(' + str(i) + ')'
  #    i += 1
  #  self.loaded_kmls.update({newName:{'data':kmlObj, 'selected':True}})
  #  
  #  return newName
  
  #def addKMLFromPath(self, path, filename):
  #  kmlObj = kmlData.KMLObject.parseKML(path)
  #  name = filename
  #  i = 1
  #  while self.loaded_kmls.has_key(name):
  #    name = filename + '(' + str(i) + ')'
  #    i += 1
  #  self.loaded_kmls.update({name:{'data':kmlObj, 'selected':True}})
  #  
  #  return name, kmlObj
  
  def getPolygonFromPlacemark(self, placemark):
    polygon = []
    for i in range(len(placemark.polygon)):
      coords = placemark.polygon[i].split(',')
      polygon.append((float(coords[0]),float(coords[1])))
    
    return polygon
  
  def getSelectedPolygons(self):
    selection = {}
    for kml in self.loaded_kmls:
      if self.loaded_kmls[kml]['selected']:
        selection.update({kml:self.loaded_kmls[kml]['data']})
    
    print selection
    
    return selection

if __name__ == '__main__':
  MapApp().run()  


