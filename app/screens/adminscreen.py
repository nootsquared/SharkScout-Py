import json
import requests
from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from kivy.uix.textinput import TextInput

class AdminScreen(Screen):
    #tba_input = TextInput(id='tba_input')

    def submit(self):
        event_key = self.ids.tba_input.text
        self.update_event_data(event_key)

    def update_event_data(self, event_key):
        api_key = "77pWgvCwlub26uzZrBULpTz5w9YqMIb9GmMg0a8hvTVEz6IaaVazvUkjgDYNBRdu"

        team_url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams/simple"
        match_url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches/simple"

        headers = {"X-TBA-Auth-Key": api_key}

        try:
            team_response = requests.get(team_url, headers=headers)
            team_response.raise_for_status()
            teams = team_response.json()

            match_response = requests.get(match_url, headers=headers)
            match_response.raise_for_status()
            matches = match_response.json()

            filtered_matches = [match for match in matches if match['comp_level'] == 'qm']

            reformatted_data = []
            for match in filtered_matches:
                for i, team_key in enumerate(match['alliances']['red']['team_keys']):
                    team = next((team for team in teams if team['key'] == team_key), None)
                    if team:
                        reformatted_data.append({
                            'match': match['match_number'],
                            'team': f"{team['team_number']} {team['nickname']}",
                            'alliance': f"R{i+1}"
                        })
                for i, team_key in enumerate(match['alliances']['blue']['team_keys']):
                    team = next((team for team in teams if team['key'] == team_key), None)
                    if team:
                        reformatted_data.append({
                            'match': match['match_number'],
                            'team': f"{team['team_number']} {team['nickname']}",
                            'alliance': f"B{i+1}"
                        })

            with open("tba.json", "w") as outfile:
                json.dump(reformatted_data, outfile, indent=4)

            print("Reformatted data retrieved and stored in reformatted_data.json")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def export_data(self):
        root = Tk()
        root.withdraw()

        output_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        output_pit_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

        with open('output.json', 'r') as output_file, open('outputpit.json', 'r') as output_pit_file:
            output_data = json.load(output_file)
            output_pit_data = json.load(output_pit_file)

        with open(output_path, 'w') as downloaded_output_file, open(output_pit_path, 'w') as downloaded_output_pit_file:
            json.dump(output_data, downloaded_output_file, indent=4)
            downloaded_output_file.write('\n')
            json.dump(output_pit_data, downloaded_output_pit_file, indent=4)
            downloaded_output_pit_file.write('\n')

    def delete_data(self):
        with open('output.json', 'w') as output_file, open('outputpit.json', 'w') as output_pit_file:
            output_file.write('')
            output_pit_file.write('')
