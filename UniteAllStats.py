import copy
import os
import pickle
import traceback

from tqdm import tqdm

import Constants
import Constants as con


def get_data(path):
    return pickle.load(open(f'{con.MAIN_PATH}{path}', "rb"))


class UniteData:
    def __init__(self):
        self.main_match_list = []
        self.match_data = get_data("Data/Matches/MatchesData/match_complete.pkl")
        self.tournaments_stats = get_data("Data/TournamentsStats/Stats/tours_complete.pkl")
        self.teams_stats = get_data("Data/TeamsOverview/Stats/team_overview_complete.pkl")
        self.teams_maps = get_data("Data/TeamsMapsStats/Stats/team_maps_stats_complete.pkl")
        self.last_5_matches_links_list = get_data("Data/Last5Matches/filtered_matches_data.pkl")
        self.result_pages_data = get_data("Data/Results/All/results_complete.pkl")
        self.train = []
        self.target = []

    def go_every_match(self):
        for match_id in tqdm(list(self.match_data.keys())[:]):
            match_data = self.match_data[match_id]
            if match_id in ["2368849_entropiq-vs-koi-pgl-cs2-major-copenhagen-2024-europe-rmr-open-qualifier-1",
                            "2368843_koi-vs-k10-pgl-cs2-major-copenhagen-2024-europe-rmr-open-qualifier-1"]:
                # print("skip KOI")
                continue
            # print(match_id, match_data)

            players = [match_data["players"][:5] + match_data["players"][5:],
                       match_data["players"][5:] + match_data["players"][:5]]

            team_index = 0
            for team1, team2 in [[match_data["team1"], match_data["team2"]],
                                 [match_data["team2"], match_data["team1"]]]:

                try:
                    values_list = [match_data["is_grand_final"], match_data["maps_count"], match_data["who_picked"]]
                    stars, result = self.get_stars_and_result(match_data["date"], match_id, team1)
                    values_list.append(stars)
                    values_list += self.get_tour_stats(match_data["tournament_link"])
                    values_list += self.get_teams_overview_stats(team1, team2, match_data["date"])
                    values_list += self.get_last_5_matches_stats(team1, team2, match_id)
                    values_list += self.get_players_stats(players[team_index], match_data["date"])
                except:
                    # print(traceback.format_exc())
                    print("bad match:", match_id)
                    continue

                # for val_index, value in enumerate(values_list):
                #     print(f"{Constants.ALL_KEYS[val_index]}: {value}")
                # print("-=" * 100)

                self.train.append(values_list)
                self.target.append(result)

                team_index = 1
        print(f"len self.train: {len(self.train)}" )
        print(f"len self.train: {len(self.target)}" )

    def get_tour_stats(self, link):
        data = self.tournaments_stats[link]
        values_list = [data["prize_pool"], data["for_invite"], data["is_lan"], data["start_date"], data["tour_type"]]
        return values_list

    def get_teams_overview_stats(self, team1, team2, date):
        values_list = []
        for team in [team1, team2]:
            stats = self.teams_stats[f"{team}_{date}"]
            for val in list(stats.values()):
                values_list.append(val)

        for team in [team1, team2]:
            team_stats = copy.deepcopy(self.teams_maps[f"{team}_{date}"])
            stats = []
            for val_index, val in enumerate(team_stats):
                stats.append(val)
                if stats[val_index][0] is not None:
                    stats[val_index][0] = Constants.MAP_POOL.index(stats[val_index][0])
            values_list.append(stats)

        return values_list

    def get_last_5_matches_stats(self, team1, team2, match_id):
        stats_list = [[], []]
        # print(team1, team2, match_id)
        for team_index, team in enumerate([team1, team2]):
            links = self.last_5_matches_links_list[match_id][team]
            for link in links:
                key = link.replace("https://www.hltv.org/stats/matches/mapstatsid/", "")
                key = key.replace("/", "_").replace("&contextTypes=team", "").replace("?", "(1)")
                stats = get_data(f"Data/Last5Matches/Stats/{team}_{key}.pkl")
                features_list = list(stats.values())[3:]
                features_list[4] = Constants.MAP_POOL.index(features_list[4])
                stats_list[team_index].append(features_list)
        return stats_list

    def get_players_stats(self, players, date):
        players_stats = []
        date = date - (date % 86400)
        for player in players:
            player = self.edit_player_name(player)
            player_data = get_data(f"Data/PlayersStats/Stats/{player}{date}.pkl")
            features_list = list(player_data.values())[1:]
            players_stats.append(features_list)
        return players_stats

    def get_stars_and_result(self, date, match_id, team1):
        date -= date % 86400
        for match in self.result_pages_data[date]:
            link = match["link"].replace('https://www.hltv.org/matches/', "").replace("/", "_")
            if link == match_id:
                # print(match)
                winner = 0 if int(match["score1"]) > int(match["score2"]) else 1
                if match["team1"] != team1:
                    winner = (winner - 1) * -1
                return winner, match["stars"]
        return 0, 0

    def edit_player_name(self, player_name):
        player_name = player_name.lower().replace("-", "")
        player_name = player_name.replace(" ", "").replace("Š", "").replace("ś", "").replace("ó", "")
        player_name = player_name.replace("_", "").replace("ı", "").replace("š", "")
        return player_name
