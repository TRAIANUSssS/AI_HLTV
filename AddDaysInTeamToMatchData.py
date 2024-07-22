import os
import pickle

import Constants as con


def get_matches_data():
    return pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))


class AddDaysInTeam:
    def __init__(self):
        self.all_matches_data = get_matches_data()

    def go_every_match(self):
        self.edit_bad_files_names()
        for key in list(self.all_matches_data.keys())[:]:
            players_list = self.all_matches_data[key]["players"]
            players_days_in_team = []
            date = self.all_matches_data[key]["date"]
            for player_index, player_name in enumerate(players_list):
                player_name = self.edit_player_name(player_name)
                current_team = self.all_matches_data[key]["team1"] if player_index < 5 else self.all_matches_data[key][
                    "team2"]
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
                        players_days_in_team.append((date - players_dates[date_index]) // 86400)
                    else:
                        players_days_in_team.append(0)
                    # print(player_name, players_days_in_team[-1], current_team, players_date_info[players_dates[date_index]], date, players_dates[date_index])
                else:
                    players_days_in_team.append(-1)
                    print(player_name, "https://www.hltv.org/matches/" + key.replace("_", "/", 1))

            print(players_days_in_team, key)

    def edit_player_name(self, player_name):
        player_name = player_name.replace("-", "")
        player_name = player_name.replace(" ", "").replace("Š", "").replace("ś", "").replace("ó", "")
        player_name = player_name.replace("_", "").replace("ı", "")
        return player_name

    def edit_bad_files_names(self):
        files = os.listdir(f'{con.MAIN_PATH}Data/PlayersStats/AllMatches')
        for file in files:
            if file.count(" ") or file.count("-"):
                data = pickle.load(open(f'{con.MAIN_PATH}Data/PlayersStats/AllMatches/{file}', "rb"))
                pickle.dump(data, open(f'{con.MAIN_PATH}Data/PlayersStats/AllMatches/{file.replace("-", "")}', "wb"))
                os.remove(f'{con.MAIN_PATH}Data/PlayersStats/AllMatches/{file}')
                print(file)
