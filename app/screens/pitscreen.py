from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivy.app import App
import json
from .homescreen import MainScreen
import qrcode
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

main_screen = MainScreen()
current_scouter = main_screen.current_scouter
#shooting speed?

class PitScreen(Screen):
    def __init__(self, **kwargs):
        super(PitScreen, self).__init__(**kwargs)
        self.drive_train = ""
        self.fit_under_stage = ""
        self.intake_description = ""
        self.scoring_position = ""
        self.hang_or_park = ""
        self.buddy_climb = ""
        self.score_via_trap = ""
        self.under_stage = ""

    def reset_values(self):
        self.drive_train = ""
        self.fit_under_stage = ""
        self.intake_description = ""
        self.scoring_position = ""
        self.hang_or_park = ""
        self.buddy_climb = ""
        self.score_via_trap = ""
        self.under_stage = ""


    def set_drive_train(self, value):
        self.drive_train = value
        print(self.drive_train)
        print("uashfda")

    def set_fit_under_stage(self, value):
        self.fit_under_stage = value

    def set_intake_description(self, value):
        self.intake_description = value

    def set_scoring_position(self, value):
        self.scoring_position = value

    def set_hang_or_park(self, value):
        self.hang_or_park = value

    def set_buddy_climb(self, value):
        self.buddy_climb = value

    def set_score_via_trap(self, value):
        self.score_via_trap = value

    def set_under_stage(self, value):
        self.under_stage = value

    

    def submit_data(self):
        print(self.drive_train)
        data = {
            'scouter_name': current_scouter,
            'team_number': self.ids.team_number_pit.text,
            'drive_train': self.drive_train,
            'fit_under_stage': self.fit_under_stage,
            'intake_description': self.intake_description,
            'scoring_position': self.scoring_position,
            'shooting_location': self.ids.shooting_location_pit.text,
            'hang_or_park': self.hang_or_park,
            'buddy_climb': self.buddy_climb,
            'score_via_trap': self.score_via_trap,
            'under_stage': self.under_stage,
            'notes': self.ids.additional_comments_pit.text,
        }

        file_path = 'outputpit.json'
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
            new_screen = PitScreen(name=self.name)
            app.root.add_widget(new_screen)
            app.root.current = new_screen.name

        done_button.bind(on_release=on_done_button_click)

        # Open the popup
        popup.open()




