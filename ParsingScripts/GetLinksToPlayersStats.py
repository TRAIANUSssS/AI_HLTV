import pickle

import Constants as con


class GetLinks:
    def __init__(self):
        self.all_matches_data = {}
        self.keys_in_filtered_data = []
        self.filtered_players_links = {}
        self.all_players_links = []

    def get_links(self):
        self.get_matches_pages()
        self.filter_data()
        self.set_filtered_data()
        self.save_filtered_links()
        self.save_all_players_links()
        self.print_data()

    def filter_data(self):
        for key in (self.all_matches_data.keys()):
            match_data = self.all_matches_data[key]
            date = match_data["date"]
            date = date - (date % 86400)
            if date not in self.keys_in_filtered_data:
                self.keys_in_filtered_data.append(date)
                links = []
            else:
                links = self.filtered_players_links[date]

            for player_link in list(match_data["players_links"].values()):
                links.append(player_link)
                self.all_players_links.append(player_link)
            self.filtered_players_links[date] = links

    def set_filtered_data(self):
        self.all_players_links = list(set(self.all_players_links))

        for key in list(self.filtered_players_links.keys()):
            self.filtered_players_links[key] = list(set(self.filtered_players_links[key]))

    def print_data(self):
        counter = 0
        for key in list(self.filtered_players_links.keys()):
            counter += len(self.filtered_players_links[key])
            # print(key, len(self.filtered_players_links[key]))
        print(f"filtered players count {counter}")
        print(f"all players links count {len(self.all_players_links)}")


    def get_matches_pages(self):
        self.all_matches_data = pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

    def save_filtered_links(self):
        pickle.dump(self.filtered_players_links,
                    open(f'{con.MAIN_PATH}Data/PlayersStats/filtered_players_links.pkl', "wb"))

    def save_all_players_links(self):
        pickle.dump(self.all_players_links,
                    open(f'{con.MAIN_PATH}Data/PlayersStats/all_players_links.pkl', "wb"))
