import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.text import LabelBase
from screens.homescreen import MainScreen
from screens.pitscreen import PitScreen
from screens.matchscreen import MatchScreen
from screens.adminscreen import AdminScreen
from stylefilecompiler import FileComplier


class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        LabelBase.register(
            name="Roboto",
            fn_regular="fonts/arial.ttf",
        )
        LabelBase.register(
            name="Roboto1",
            fn_regular="fonts/opensans.ttf",
        )

        FileComplier.combineFiles()

        kv = Builder.load_file("mainstyling.kv")

        self.sm.add_widget(MainScreen(name='home'))
        self.sm.add_widget(PitScreen(name='pits'))
        self.sm.add_widget(MatchScreen(name='match'))
        self.sm.add_widget(AdminScreen(name='admin'))
        self.sm.current = 'match'
        return kv

if __name__ == "__main__":
    MainApp().run()
