import requests
import json
import pandas as pd
from src.CONSTANS import MAIN_API


class Refresher:

    def api_call(self, api):
        api_result = requests.get(api).json()
        return api_result

    def update_events(self):
        api_result = self.api_call(MAIN_API)
        df_events = pd.json_normalize(api_result['events'])
        return df_events

    def update_players(self):
        api_result = self.api_call(MAIN_API)
        df_players = pd.json_normalize(api_result['elements'])
        return df_players 

    def update_teams(self):
        api_result = self.api_call(MAIN_API)
        df_teams = pd.json_normalize(api_result['teams'])
        return df_teams 