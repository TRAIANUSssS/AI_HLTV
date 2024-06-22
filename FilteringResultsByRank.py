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
                    print(match_info)

                    match_info["score1"], match_info["score2"] = int(match_info["score1"]), int(match_info["score2"])
                    self.filtered_results_data[result_date].append(match_info)

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
