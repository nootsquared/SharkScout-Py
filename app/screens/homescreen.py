from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

class MainScreen(Screen):
    current_scouter = StringProperty("Pranav_M")

    def change_scouter(self, new_scouter):
        self.current_scouter = new_scouter

    def submit_name(self):
        current_name = self.ids.name_input.text
        self.change_scouter(current_name)
