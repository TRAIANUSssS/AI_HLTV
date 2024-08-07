import pickle
import time
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_structure = {
    "date_1": {
        "teams": ["team1", "team2"],
        "placements": {
            "team1": 1,
            "team2": 2,
        },
        "points": {
            "team1": 200,
            "team2": 100,
        }

    },
    "date_2": {
        "teams": ["team2", "team1"],
        "placements": {
            "team2": 1,
            "team1": 2,
        },
        "points": {
            "team2": 500,
            "team1": 200,
        }
    }
}


class RankingParsing:
    def __init__(self, parsing=True):
        self.parsing = parsing
        self.start_with_week = 0
        self.total_weeks_count = 150
        self.current_week_parsed = 0
        self.start_date = 1718582400  # 2024 17th june
        self.current_date = self.start_date
        self.info_dict = {}
        self.year = 0
        self.month = ""
        self.day = 0

    def go_every_week(self):
        self.current_date -= self.start_with_week * 24 * 360 * 7
        for current_week_num in tqdm(range(self.total_weeks_count)):
            self.get_date_for_request()

            soup = self.get_page()
            if soup is not None:
                try:
                    self.get_data(soup)
                    self.save_into_pickle_file()
                    self.clear_info_dict()
                    time.sleep(0.1)
                except:
                    print(traceback.format_exc())

            self.current_week_parsed += 1
            self.current_date -= 24 * 3600 * 7

    def get_date_for_request(self):
        self.year = int(time.strftime('%Y', time.localtime(self.current_date)))
        self.month = int(time.strftime('%m', time.localtime(self.current_date)))
        self.day = int(time.strftime('%d', time.localtime(self.current_date)))

        self.month = con.MONTHS[self.month]
        # print(self.year, self.month, self.day, )

    def get_page(self):
        response = requests.get(f'https://www.hltv.org/ranking/teams/{self.year}/{self.month}/{self.day}',
                                headers=con.headers_for_ranking_stats)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_data(self, soup):
        self.info_dict[self.current_date] = {"teams": [], "placements": {}, "points": {}}
        all_lines = soup.find_all("div", {"class": "ranked-team standard-box"})

        for line in all_lines:
            team_name = line.find("span", {"class": "name"}).text
            team_rank = int(line.find("span", {"class": "position"}).text.replace("#", ""))
            team_points = line.find("span", {"class": "points"}).text
            team_points = int(''.join(filter(str.isdigit, team_points)))

            self.info_dict[self.current_date]["teams"].append(team_name)
            self.info_dict[self.current_date]["placements"][team_name] = team_rank
            self.info_dict[self.current_date]["points"][team_name] = team_points

        # print(self.info_dict)

    def clear_info_dict(self):
        self.info_dict = {}

    def save_into_pickle_file(self):
        pickle.dump(self.info_dict,
                    open(f'{con.MAIN_PATH}Data/Ranking/ranking_stats_week_{self.current_week_parsed}.pkl', "wb"))

    def fill_empty_data(self):
        pass

    def unite_all_pickle_files(self):
        united_dict = {}
        for week_num in tqdm(range(self.total_weeks_count)):
            current_data = pickle.load(open(f'{con.MAIN_PATH}Data/Ranking/ranking_stats_week_{week_num}.pkl', "rb"))
            united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/Ranking/ranking_complete.pkl', "wb"))
