
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import *
from kivy.lang import Builder

label_entry = """
MDTextField:
   hint_text: "Enter Watering Time"
   helper_text: "NOTE: Value in hours"
   helper_text_mode: "on_focus"
   icon_right: "android"
   icon_right_color: app.theme_cls.primary_color
   pos_hint: {'center_x': 0.5, 'center_y': 0.5}
   size_hint_x: None
   width: 300
"""
class MyApp(MDApp):
    def build(self):
        global MyLabel
        screen = Screen()
        self.theme_cls.primary_palette="Green"     #color scheme of the whole program
        MyLabel = Builder.load_string(label_entry)
        button = MDFillRoundFlatButton(text="DONE",pos_hint= {'center_x': 0.5, 'center_y': 0.4}, on_release=self.show)
        ONbutton = MDFillRoundFlatButton(text="ON", pos_hint={'x': 0.8, 'y': 0.8}, on_release=self.ON)
        OFFbutton = MDRoundFlatButton(text="OFF", pos_hint={'X': 0.7, 'y': 0.8}, on_release=self.OFF)
        screen.add_widget(MyLabel)
        screen.add_widget(ONbutton)
        screen.add_widget(OFFbutton)
        screen.add_widget(button)
        return screen

    def show(self,obj):
        pass

    def ON(self, obj):
        pass

    def OFF(self, obj):
        pass

MyApp().run()
