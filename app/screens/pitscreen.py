from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivy.app import App
import json
from .homescreen import MainScreen

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
            'name': current_scouter,
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
            'other_notes': self.ids.additional_comments_pit.text,
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

        self.reset_values()
        app = App.get_running_app()
        old_screen = app.root.get_screen(self.name)
        app.root.remove_widget(old_screen)
        new_screen = PitScreen(name=self.name)
        app.root.add_widget(new_screen)
        app.root.current = new_screen.name




