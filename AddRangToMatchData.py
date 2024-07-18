import pickle

import Constants as con


def get_rang_data():
    return pickle.load(open(f'{con.MAIN_PATH}Data/Ranking/ranking_complete.pkl', "rb"))


def get_matches_data():
    return pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))


class AddRang:
    def __init__(self):
        self.rang_data = get_rang_data()
        self.matches_data = get_matches_data()

    def go_every_match(self):
        all_dates = list(self.rang_data.keys())
        for key in list(self.matches_data.keys()):
            data = self.matches_data[key]
            team1, team2 = data["team1"], data["team2"]
            curr_time = self.matches_data[key]["date"]
            curr_time -= curr_time % (24 * 3600)
            while curr_time not in all_dates:
                curr_time -= 24 * 3600

            exist_team1 = team1 in self.rang_data[curr_time]["teams"]
            exist_team2 = team2 in self.rang_data[curr_time]["teams"]

            self.matches_data[key]["rang1"] = self.rang_data[curr_time]["placements"][team1] if exist_team1 else 40
            self.matches_data[key]["rang2"] = self.rang_data[curr_time]["placements"][team2] if exist_team2 else 40
            self.matches_data[key]["points1"] = self.rang_data[curr_time]["points"][team1] if exist_team1 else 10
            self.matches_data[key]["points2"] = self.rang_data[curr_time]["points"][team2] if exist_team2 else 10
            # print(self.matches_data[key])
        self.save_all_matches_data()

    def save_all_matches_data(self):
        pickle.dump(self.matches_data, open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "wb"))
