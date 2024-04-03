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
from kivy.properties import StringProperty
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
    r1 = StringProperty("N/A")
    r2 = StringProperty("N/A")
    r3 = StringProperty("N/A")
    b1 = StringProperty("N/A")
    b2 = StringProperty("N/A")
    b3 = StringProperty("N/A")

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

    def submit_match_num(self, qual_number):
        with open('tba.json') as f:
            data = json.load(f)

        alliances = {"R1": "", "R2": "", "R3": "", "B1": "", "B2": "", "B3": ""}
        self.matchnumber = qual_number

        for entry in data:
            if entry['match'] == int(qual_number):
                alliances[entry['alliance']] = entry['team'].split()[0]

        self.r1 = alliances['R1']
        self.r2 = alliances['R2']
        self.r3 = alliances['R3']
        self.b1 = alliances['B1']
        self.b2 = alliances['B2']
        self.b3 = alliances['B3']

        self.ids.r1_label.text = f"R1: {self.r1}"
        self.ids.r2_label.text = f"R2: {self.r2}"
        self.ids.r3_label.text = f"R3: {self.r3}"
        self.ids.b1_label.text = f"B1: {self.b1}"
        self.ids.b2_label.text = f"B2: {self.b2}"
        self.ids.b3_label.text = f"B3: {self.b3}"
    

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

        self.selectedteam = ''
        self.matchnumber = ''
    
    def selected_team(self, value):
        print(f"Selected team: {value}")
        self.selectedteam = value

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
            'scouter_name': current_scouter,
            'match_number': self.matchnumber,
            'team_number': self.selectedteam,
            #alliance
            'starting_position': self.starting_place,
            'amp_notes_auton': self.auton_amp,
            'speaker_notes_auton': self.auton_speaker,
            'additional_notes_location': self.note_pickup,
            'left_starting_zone': self.left_starting_zone,
            'amp_notes_teleop': self.teleop_amp,
            'speaker_notes_teleop': self.teleop_speaker,
            'trap': self.trap,
            'hang_or_park': self.climbed,
            'harmonize': self.harmonized,
            'robot_driving': self.robot_driving,
            'defense_capability': self.defense_capabilities,
            'notes': self.ids.other_notes.text,
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
#{"scouter_name": "Zach", "match_number": "78", "team_number": "573", "alliance": "Blue", "starting_position": "Source", "amp_notes_auton": "0", "speaker_notes_auton": "1", "additional_notes_location": "Center line", "amp_notes_teleop": "0", "speaker_notes_teleop": "2", "trap": "No", "hang_or_park": "None", "harmonize": "No", "robot_driving": "Poor", "defense_capability": "Did not play defense", "notes": "Robot broke down at the source at around 1:45 and didn't start again", "totalAutonPoints": 1, "totalTeleopPoints": 2},
#{"name":"Pranav_M","starting_place":"Center","note_pickup":"Both","left_starting_zone":"","auton_speaker":0,"auton_amp":0,"teleop_speaker":0,"teleop_amp":0,"trap":"","harmonized":"","climbed":"","robot_driving":"","defense_capabilities":"","other_notes":""}
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

