import copy
import os
import pickle
import traceback

from tqdm import tqdm

import Constants
import Constants as con


class EditAllStats:
    def __init__(self):
        self.train = pickle.load(open(f"{Constants.MAIN_PATH}/Data/FinalData/train.pkl", "rb"))
        self.target = pickle.load(open(f"{Constants.MAIN_PATH}/Data/FinalData/target.pkl", "rb"))
        self.first = True
        self.maps_stats_count = 0
        self.maps_stats_len_avg = 0
        self.maps_stats_len_max = 0
        self.maps_stats_len_min = 100
        self.last_5_matches_one_match_count = 0
        self.last_5_matches_one_match_avg = 0
        self.last_5_matches_one_match_max = 0
        self.last_5_matches_one_match_min = 100
        self.last_5_matches_one_match_list = [0] * 72

    def go_every_match(self):
        [print(val) for val in self.train[0]]
        complete_new_data = []
        for match_data in self.train:
            new_data = []
            for iteration, item in enumerate(match_data):
                it_result = self.working_with_every_iteration(iteration, item)
                if it_result is not None:
                    new_data += it_result
                else:
                    break
            else:
                if len(new_data) == 8217:
                    complete_new_data.append(new_data)

        self.print_data(complete_new_data)

    def working_with_every_iteration(self, iteration, item):
        iteration_data = []
        if iteration == 2:  # who picked first
            iteration_data.append(item[0])
        elif iteration == 23 or iteration == 24:  # add empty maps is it need
            iteration_data.append("maps_data" + "+" * 100)
            matches_data = []
            matches_count = len(item)
            for match_index in range(5):
                if match_index >= matches_count or item[match_index][0] is None:
                    matches_data += [-1, -1, -1, -1, -1, -1]
                else:
                    matches_data += item[match_index]
            iteration_data += matches_data
        elif iteration == 25 or iteration == 26:  # working with last 5 matches
            iteration_data.append("last_5_matches_data" + "+" * 100)

            for match in item:
                # self.get_last_5_matches_one_stats_len(match[17])
                if len(match[17]) > 54:
                    return None
                iteration_data += match[:17]
                iteration_data += match[17] + [-1] * (54 - len(match[17]))
                iteration_data += match[18] + [-1] * (54 - len(match[18]))
                iteration_data += self.get_players_stats_from_last_5_matches(match[19])
            iteration_data += [-1] * 205 * (19 - len(item))  # 19 - max_maps_count, 205 values in every map
        elif 26 < iteration < 37:
            iteration_data.append("players_stats" + "+" * 100)
            if len(item[10]) == 10:
                return None
            iteration_data += item[:10] + item[12:15] + item[16:]
            iteration_data += item[10] + item[11] + item[15]
        else:
            iteration_data.append(item)

        return iteration_data

    def print_data(self, complete_new_data):
        # print("-=" * 100)
        # [print(val) for val in complete_new_data[0]]
        # print("-=" * 100)
        print(f"total matches: {len(complete_new_data)}")
        len_counts = [len(val) for val in complete_new_data]
        print(f"total_len_min: {min(len_counts)}")
        print(f"total_len_max: {max(len_counts)}")
        print(f"total_len_min count: {len_counts.count(min(len_counts))}")
        print(f"total_len_max count: {len_counts.count(max(len_counts))}")

    def get_maps_stats_len(self, maps_stats):
        _len = len(maps_stats)
        self.maps_stats_count += 1
        self.maps_stats_len_avg = (self.maps_stats_len_avg * (self.maps_stats_count - 1) + _len) / self.maps_stats_count
        self.maps_stats_len_max = _len if _len > self.maps_stats_len_max else self.maps_stats_len_max
        self.maps_stats_len_min = _len if _len < self.maps_stats_len_min else self.maps_stats_len_min

    def get_last_5_matches_one_stats_len(self, maps_stats):
        _len = len(maps_stats)
        self.last_5_matches_one_match_count += 1
        self.last_5_matches_one_match_avg = (self.last_5_matches_one_match_avg * (
                self.last_5_matches_one_match_count - 1) + _len) / self.last_5_matches_one_match_count
        self.last_5_matches_one_match_max = _len if _len > self.last_5_matches_one_match_max else self.last_5_matches_one_match_max
        self.last_5_matches_one_match_min = _len if _len < self.last_5_matches_one_match_min else self.last_5_matches_one_match_min
        self.last_5_matches_one_match_list[_len] += 1

    def get_players_stats_from_last_5_matches(self, match):
        players_stats = []
        for team_index in range(2):
            for player_index in range(5):
                for stat_index in range(8):
                    players_stats += [match[team_index][player_index][stat_index]]
        return players_stats
