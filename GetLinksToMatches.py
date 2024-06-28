import pickle

import Constants as con


class GetLinks:
    def __init__(self):
        self.all_matches_data = {}
        self.all_teams_maps = {}
        self.filtered_matches_data = {}
        self.filtered_matches_data_for_parsing = []

    def get_links(self):
        self.get_matches_pages()
        self.get_all_teams_maps()
        self.filtering_matches_data()
        self.get_matches_for_parsing()
        self.save_matches_for_parsing()
        self.save_filtered_matches()

    def get_matches_for_parsing(self):
        for value in list(self.filtered_matches_data.values()):
            self.filtered_matches_data_for_parsing += value

        print("len", len(self.filtered_matches_data_for_parsing))
        self.filtered_matches_data_for_parsing = list(set(self.filtered_matches_data_for_parsing))
        print("len", len(self.filtered_matches_data_for_parsing))

    def filtering_matches_data(self):
        for match_id in self.all_matches_data.keys():
            date = self.all_matches_data[match_id]["date"]
            date = date - (date % 86400)
            team1, team2 = self.all_matches_data[match_id]["team1"], self.all_matches_data[match_id]["team2"]
            prev_matches_list = []
            for team in [team1, team2]:
                # print(date, self.all_matches_data[match_id]["team1_link"])
                # print(self.all_teams_maps[team]["all_played_maps"])
                start_index = self.get_match_index(date, self.all_teams_maps[team]["all_played_dates"])

                matches_found = 0
                find_current_match = False
                prev_opponent = ""

                for match_index in range(start_index, len(self.all_teams_maps[team]["all_played_dates"])):
                    match_date = self.all_teams_maps[team]["all_played_maps"][match_index]
                    if matches_found == 5 and prev_opponent != match_date["opponent"]:
                        break
                    if match_date["opponent"] == team2:
                        find_current_match = True
                        continue
                    elif find_current_match and match_date["opponent"] != team2:
                        # prev_match_data = [match_date["match_link"], match_date["is_first_map"],
                        #                    match_date["is_first_match"]]
                        prev_matches_list.append(match_date["match_link"])
                        if prev_opponent != match_date["opponent"]:
                            prev_opponent = match_date["opponent"]
                            matches_found += 1

            self.filtered_matches_data[match_id] = prev_matches_list
            # print(self.filtered_matches_data[match_id])

    def get_match_index(self, date, all_dates):
        if len(all_dates) == 0 or all_dates[-1] < date:
            return -1

        return all_dates.index(date)

    def get_matches_pages(self):
        self.all_matches_data = pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

    def get_all_teams_maps(self):
        self.all_teams_maps = pickle.load(open(f'{con.MAIN_PATH}Data/TeamsMaps/Pages/match_complete.pkl', "rb"))

    def save_matches_for_parsing(self):
        pickle.dump(self.filtered_matches_data_for_parsing,
                    open(f'{con.MAIN_PATH}Data/Last5Matches/filtered_matches_data_for_parsing.pkl',
                         "wb"))

    def save_filtered_matches(self):
        pickle.dump(self.filtered_matches_data,
                    open(f'{con.MAIN_PATH}Data/Last5Matches/filtered_matches_data.pkl',
                         "wb"))
