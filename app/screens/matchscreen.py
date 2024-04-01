from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
import json
from kivy.clock import Clock
from kivy.app import App
from .homescreen import MainScreen
import qrcode
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.label import Label
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)

main_screen = MainScreen()
current_scouter = main_screen.current_scouter

class MatchScreen(Screen):
    auton_speaker = NumericProperty(0)
    auton_amp = NumericProperty(0)
    teleop_speaker = NumericProperty(0)
    teleop_amp = NumericProperty(0)

    def increment1(self):
        self.auton_speaker += 1

    def decrement1(self):
        if self.auton_speaker > 0:
            self.auton_speaker -= 1

    def increment2(self):
        self.auton_amp += 1
    
    def decrement2(self):
        if self.auton_amp > 0:
            self.auton_amp -= 1

    def increment3(self):
        self.teleop_speaker += 1
    
    def decrement3(self):
        if self.teleop_speaker > 0:
            self.teleop_speaker -= 1
    
    def increment4(self):
        self.teleop_amp += 1
    
    def decrement4(self):
        if self.teleop_amp > 0:
            self.teleop_amp -= 1
    

    def __init__(self, **kwargs):
        super(MatchScreen, self).__init__(**kwargs)
        self.starting_place = ""
        self.note_pickup = ""
        self.left_starting_zone = ""
        self.trap = ""
        self.harmonized = ""
        self.climbed = ""
        self.robot_driving = ""
        self.defense_capabilities = ""

    def set_starting_place(self, value):
        self.starting_place = value

    def set_note_pickup(self, value):
        self.note_pickup = value

    def set_left_starting_zone(self, value):
        self.left_starting_zone = value

    def set_trap(self, value):
        self.trap = value

    def set_harmonized(self, value):
        self.harmonized = value

    def set_climbed(self, value):
        self.climbed = value

    def set_robot_driving(self, value):
        self.robot_driving = value

    def set_defense_capabilities(self, value):
        self.defense_capabilities = value
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    def submit_data(self):
        
        data = {
            'name': current_scouter,
            'starting_place': self.starting_place,
            'note_pickup': self.note_pickup,
            'left_starting_zone': self.left_starting_zone,
            'auton_speaker': self.auton_speaker,
            'auton_amp': self.auton_amp,
            'teleop_speaker': self.teleop_speaker,
            'teleop_amp': self.teleop_amp,
            'trap': self.trap,
            'harmonized': self.harmonized,
            'climbed': self.climbed,
            'robot_driving': self.robot_driving,
            'defense_capabilities': self.defense_capabilities,
            'other_notes': self.ids.other_notes.text,
        }

        file_path = 'output.json'
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        existing_data.append(data)

        with open(file_path, 'w') as f:
            f.write('[\n')
            for i, item in enumerate(existing_data):
                f.write(json.dumps(item) + (',' if i < len(existing_data) - 1 else '') + '\n')
            f.write(']\n')

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(json.dumps(data))
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode.png')

        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode.png')

        # Create a popup with the QR code and a "Done" button
        # Create a popup with the QR code and a "Done" button
        layout = BoxLayout(orientation='vertical')
        qr_image = Image(source='qrcode.png')
        qr_image.reload()

        # Create the "Done" button with a size hint and position hint
        done_button = Button(text='Done', size_hint=(.3, .1), pos_hint={'center_x': .5})

        # Add a padding of 50px between the image and the button
        # Add a padding of 25px at the top of the layout
        layout.add_widget(Label(size_hint_y=None, height=25))  # This is the padding
        layout.add_widget(qr_image)
        layout.add_widget(Label(size_hint_y=None, height=25))  # This is the padding
        layout.add_widget(done_button)

        popup = Popup(content=layout, auto_dismiss=False, title_size=0, separator_height=0)


        # When the "Done" button is clicked, close the popup and reset the screen
        def on_done_button_click(instance):
            popup.dismiss()
            self.reset_values()
            app = App.get_running_app()
            old_screen = app.root.get_screen(self.name)
            app.root.remove_widget(old_screen)
            new_screen = MatchScreen(name=self.name)
            app.root.add_widget(new_screen)
            app.root.current = new_screen.name

        done_button.bind(on_release=on_done_button_click)

        # Open the popup
        popup.open()

    def reset_values(self):
        self.auton_speaker = 0
        self.auton_amp = 0
        self.teleop_speaker = 0
        self.teleop_amp = 0
        self.starting_place = ""
        self.note_pickup = ""
        self.left_starting_zone = ""
        self.trap = ""
        self.harmonized = ""
        self.climbed = ""
        self.robot_driving = ""
        self.defense_capabilities = ""
        self.ids.other_notes.text = ""

