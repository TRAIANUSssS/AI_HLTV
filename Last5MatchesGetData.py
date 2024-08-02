import datetime
import os
import pickle
import time
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con
import Last5MatchesParsing

example_dict = {
    "date": 1718150400,
    "team1": "name",
    "team2": "name",
    "rank_1": 10,
    "rank_2": 11,
    "points1": 200,
    "points2": 184,
    "map_name": "Mirage",
    "score1": 7,
    "score2": 13,
    "first_side_score1": 3,
    "first_side_score2": 10,
    "second_side_score1": 4,
    "second_side_score2": 3,
    "rating1": 1.1,
    "rating2": 1.2,
    "first_kills1": 5,
    "first_kills2": 15,
    "clutches_won1": 0,
    "clutches_won2": 2,
    "round_winners": [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    "round_history": [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    "players_stats": [[[], [], [], [], []], [[], [], [], [], []]]
}

STATS_NAMES = ["date", "team1", "team2", "rank_1", "rank_2", "points1", "points2", "map_name", "score1", "score2",
               "first_side_score1", "first_side_score2", "second_side_score1", "second_side_score2", "rating1",
               "rating2", "fist_kills1", "fist_kills2", "clutches_won1", "clutches_won2", "round_winners",
               "round_history", "players_stats"]


class Last5Matches:
    def __init__(self):
        self.parsed_data = {}
        self.match_data = []
        self.ranking_data = {}
        self.all_links = []
        self.all_html_files = os.listdir(f'{con.MAIN_PATH}Data/Last5Matches/HTML/')
        self.current_link = ""
        self.file_name = ""
        self.soup = None

    def go_every_match(self):
        self.get_all_links()
        self.get_ranking_data()

        for self.current_link in tqdm(self.all_links):
        # for self.current_link in self.all_links[:2]:
            self.file_name = self.current_link.replace("https://www.hltv.org/stats/matches/mapstatsid/", "")
            self.file_name = self.file_name.replace("/", "_").replace("&contextTypes=team", "").replace("?", "(1)")
            if f"{self.file_name}.html" in self.all_html_files:
                continue
            self.get_soup()

            if self.soup is not None:
                try:
                    self.parse_page()
                    self.working_with_variables_assignments(False)
                    self.swap_teams()
                    self.working_with_variables_assignments(False)
                    self.save_page_into_html(self.soup)

                except:
                    print(self.current_link)
                    print(traceback.format_exc())

    def parse_page(self):
        date = Last5MatchesParsing.get_date(self.soup)
        team1, team2 = Last5MatchesParsing.get_teams_names(self.soup)
        rank_1, points_1, rank_2, points_2 = self.get_rank_stats(date, team1, team2)
        map_name = Last5MatchesParsing.get_map_name(self.soup)
        score_1, score_2 = Last5MatchesParsing.get_score(self.soup)
        first_side_score1, first_side_score2, second_side_score1, second_side_score2 = Last5MatchesParsing.get_side_scors(
            self.soup)
        rating_1, rating_2 = Last5MatchesParsing.get_rating(self.soup)
        first_kills_1, first_kills_2 = Last5MatchesParsing.get_first_kills(self.soup)
        clutches_won_1, clutches_won_2 = Last5MatchesParsing.get_clutches_count(self.soup)
        round_winners, round_history = Last5MatchesParsing.get_round_history(self.soup, score_1 + score_2)
        players_stats = Last5MatchesParsing.get_players_stats(self.soup)

        self.match_data = [date, team1, team2, rank_1, rank_2, points_1, points_2, map_name, score_1, score_2,
                           first_side_score1, first_side_score2, second_side_score1, second_side_score2, rating_1,
                           rating_2, first_kills_1, first_kills_2, clutches_won_1, clutches_won_2, round_winners,
                           round_history, players_stats]

    def working_with_variables_assignments(self, _print=True):
        for stat_index, stat_name in enumerate(STATS_NAMES):
            if _print:
                print(stat_index, stat_name, self.match_data[stat_index])
            self.parsed_data[stat_name] = self.match_data[stat_index]
        if self.parsed_data["team1"] == "KOI":
            print(self.file_name)
        self.save_into_pickle_file(self.parsed_data["team1"])
        self.clear_parsed_data()

    def swap_teams(self):
        swap_index_list = [[1, 2], [3, 4], [5, 6], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]]
        for index_list in swap_index_list:
            tmp = self.match_data[index_list[0]]
            self.match_data[index_list[0]] = self.match_data[index_list[1]]
            self.match_data[index_list[1]] = tmp

        round_result_list = []
        for round_result in self.match_data[20]:
            round_result_list.append(int(not round_result))
        self.match_data[20] = round_result_list

        tmp = self.match_data[22][0]
        self.match_data[22][0] = self.match_data[22][1]
        self.match_data[22][1] = tmp

    def get_rank_stats(self, date, team1_name, team2_name):
        ranking_days = self.ranking_data.keys()
        date = date - (date % 86400)
        while date not in ranking_days:
            if date < 1624827600:
                break
            date -= 24 * 3600

        ranking_data_for_current_match = []
        for team in [team1_name, team2_name]:
            if team in self.ranking_data[date]["teams"]:
                place = self.ranking_data[date]["placements"][team]
                points = self.ranking_data[date]["points"][team]
                ranking_data_for_current_match += [place, points]
            else:
                ranking_data_for_current_match += [40, 10]

        return ranking_data_for_current_match

    def get_soup(self):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/Last5Matches/HTML/{self.file_name}.html'):
            self.soup = self.get_match_page(self.current_link)
        else:
            self.soup = self.get_exist_html_file()

    def get_match_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_teams_matches_pages)
        time.sleep(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response", self.current_link)
            return None

    def get_exist_html_file(self):
        with open(f'{con.MAIN_PATH}Data/Last5Matches/HTML/{self.file_name}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def clear_parsed_data(self):
        self.parsed_data = {}

    def get_ranking_data(self):
        self.ranking_data = pickle.load(
            open(f'{con.MAIN_PATH}Data/Ranking/ranking_complete.pkl', "rb"))

    def get_all_links(self):
        self.all_links = pickle.load(
            open(f'{con.MAIN_PATH}Data/Last5Matches/filtered_matches_data_for_parsing.pkl', "rb"))

    def save_into_pickle_file(self, name):
        pickle.dump(self.parsed_data,
                    open(f'{con.MAIN_PATH}Data/Last5Matches/Stats/{name}_{self.file_name}.pkl', "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/Last5Matches/HTML/{self.file_name}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))
