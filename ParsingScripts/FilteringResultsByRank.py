import pickle

import Constants as con


class FilteringByRank:
    def __init__(self):
        self.rank_data = {}
        self.results_data = {}
        self.filtered_results_data = {}
        self.all_ranking_dates = []
        self.all_results_dates = []
        self.current_rank_date = 0
        self.current_rank_date_num = 0
        self.ranking_dates_count = len(self.all_ranking_dates)

    def filter(self):
        self.preparing_data()
        matches_counter, maps_counter, total_matches_counter, total_maps_counter = 0, 0, 0, 0

        for result_date in self.all_results_dates:
            if result_date < self.current_rank_date:
                self.current_rank_date_num += 1
                self.current_rank_date = self.all_ranking_dates[self.current_rank_date_num]

            self.filtered_results_data[result_date] = []
            teams = self.rank_data[self.current_rank_date]["teams"]
            for match_info in self.results_data[result_date]:
                if match_info["team1"] in teams or match_info["team2"] in teams:
                    rank1, points1, rank2, points2 = self.get_rank(match_info)
                    match_info["score1"], match_info["score2"] = int(match_info["score1"]), int(match_info["score2"])
                    match_info["rank1"], match_info["rank2"] = rank1, rank2
                    match_info["points1"], match_info["points2"] = points1, points2
                    self.filtered_results_data[result_date].append(match_info)
                    print(match_info)

                    matches_counter += 1
                    total_score = int(match_info["score1"]) + int(match_info["score2"])
                    maps_counter += 1 if total_score > 13 else total_score
                total_matches_counter += 1
                total_score = int(match_info["score1"]) + int(match_info["score2"])
                total_maps_counter += 1 if total_score > 13 else total_score
            if not self.filtered_results_data[result_date]:
                del self.filtered_results_data[result_date]

        print("matches count:", matches_counter, "maps count:", maps_counter)
        print("total matches count:", total_matches_counter, "total maps count:", total_maps_counter)
        self.save_filtered_results_stats()

    def get_rank(self, match_info):
        ranks_data = []
        teams = [match_info["team1"], match_info["team2"]]
        for team in teams:
            if team in self.rank_data[self.current_rank_date]["teams"]:
                rank = self.rank_data[self.current_rank_date]["placements"][team]
                points = self.rank_data[self.current_rank_date]["points"][team]
            else:
                rank = 40
                points = 10

            ranks_data += [rank, points]
        return ranks_data

    def preparing_data(self):
        self.open_files()

        self.all_ranking_dates = list(self.rank_data.keys())
        self.all_results_dates = list(self.results_data.keys())

        self.current_rank_date = self.all_ranking_dates[0]

    def open_files(self):
        self.results_data = pickle.load(open(f'{con.MAIN_PATH}Data/Results/All/results_complete.pkl', "rb"))
        self.rank_data = pickle.load(open(f'{con.MAIN_PATH}Data/Ranking/ranking_complete.pkl', "rb"))

    def save_filtered_results_stats(self):
        pickle.dump(self.filtered_results_data,
                    open(f'{con.MAIN_PATH}Data/Results/All/results_complete_filtered.pkl', "wb"))
