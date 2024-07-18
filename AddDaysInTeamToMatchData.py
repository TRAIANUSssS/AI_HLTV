import os
import pickle

import Constants as con

def get_matches_data():
    return pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

class AddDaysInTeam:
    def __init__(self):
        self.all_matches_data = get_matches_data()

    def go_every_match(self):
        for key in list(self.all_matches_data.keys())[:5]:
            players_list = self.all_matches_data[key]["players"]
            players_days_in_team = []
            date = self.all_matches_data[key]["date"]
            for player_index, player_name in enumerate(players_list):
                current_team = self.all_matches_data[key]["team1"] if player_index < 5 else self.all_matches_data[key]["team2"]
                file_name = f'{con.MAIN_PATH}Data/PlayersStats/AllMatches/all_maps_{player_name}.pkl'
                if os.path.exists(file_name):
                    players_date_info = pickle.load(open(file_name, "rb"))
                    players_dates = players_date_info["all_dates"][::-1]
                    date_index, players_dates_len = 0, len(players_dates) - 1
                    while date_index < players_dates_len and date < players_dates[date_index]:
                        # if player_name == "MATYS":
                        #     print( date, players_dates[date_index])
                        date_index += 1
                    # print(current_team, players_date_info[players_dates[date_index]])
                    if current_team.replace(" ", "") == players_date_info[players_dates[date_index]].replace(" ", ""):
                        players_days_in_team.append((date-players_dates[date_index]) // 86400)
                    else:
                        players_days_in_team.append(0)
                    # print(player_name, players_days_in_team[-1], current_team, players_date_info[players_dates[date_index]], date, players_dates[date_index])
                else:
                    players_days_in_team.append(-1)

            print(players_days_in_team, key)
