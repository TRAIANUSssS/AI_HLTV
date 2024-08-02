import datetime
import os
import pickle
import time
import traceback

import requests
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con
import ParsePlayersStats

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

example_dict = {
    "name": "name",
    "total_kills": 12121,
    "HS": 42,
    "total_deaths": 10,
    "dmg_round": 23,
    "maps_played": 12,
    "rounds_played": 100,
    "kill_round": 0.8,
    "assist_round": 0.1,
    "death_round": 0.4,
    "rating": 1.23,
    "rating_5-30": [1.2, 1.3, 1.4, 1.5],
    "maps_5-30": [5, 6, 7, 8],
    "kast": 68.7,
    "impact": 1.13,
    "age": 21,
    "kills_0-5": [431, 232, 93, 30, 5, 1],
    "open_kills": 75,
    "open_deaths": 91,
    "open_ratio": 0.82,
    "open_rating": 0.95,
    "rifle_kills": 392,
    "sniper_kills": 4
}

STATS_NAMES = ["name", "total_kills", "HS", "total_deaths", "dmg_round", "maps_played", "rounds_played", "kill_round",
               "assist_round", "death_round", "rating", "rating_5_30", "maps_5_30", "kast", "impact", "age",
               "kills_0_5", "open_kills", "open_deaths", "open_ratio", "open_rating", "rifle_kills", "sniper_kills"]


class GetPlayersStats:
    def __init__(self):
        self.player_stats = {}
        self.filtered_players_links = {}
        self.tmp_data = []
        self.current_date = 0
        self.current_link = ""
        self.file_name = ""
        self.soup = None

    def go_every_link(self):
        self.get_filtered_players_links()
        all_files = os.listdir(f'{con.MAIN_PATH}Data/PlayersStats/Stats/')
        non_parsed_pages = []

        for self.current_date in list(self.filtered_players_links.keys()):
            for self.current_link in self.filtered_players_links[self.current_date]:
                player_name = self.current_link.split("/")[-1]
                self.file_name = f'{player_name}_{self.current_date}'
                if f"{self.file_name}.pkl" not in all_files:
                    non_parsed_pages.append([self.current_date, self.current_link])

        with tqdm(total=len(non_parsed_pages) * 2) as pbar:
            for self.current_date, self.current_link in non_parsed_pages:
                # for self.current_date in list(self.filtered_players_links.keys()):
                #     for self.current_link in self.filtered_players_links[self.current_date]:
                player_name = self.current_link.split("/")[-1]
                self.file_name = f'{player_name}_{self.current_date}'
                # if f"{self.file_name}.pkl" in all_files:
                #     pbar.update(1)
                #     continue

                for prefix in ["overview", "individual"]:
                    try:
                        self.edit_link(prefix)
                        self.get_soup(prefix)
                        if self.soup is not None:
                            if prefix == "overview":
                                self.parse_overview_page()
                            else:
                                self.parse_individual_page()
                                self.working_with_variables_assignments(False)
                                self.save_into_pickle_file()
                                self.clear_player_stats()
                            self.save_page_into_html(self.soup, prefix)
                    except:
                        print(prefix, self.current_link)
                        print(traceback.format_exc())
                    pbar.update(1)

    def parse_overview_page(self):
        name = ParsePlayersStats.get_player_name(self.soup)
        total_kills, HS, total_deaths, dmg_round, maps_played, rounds_played, kill_round, assist_round, death_round, \
            rating = ParsePlayersStats.get_stats_from_stat_box(self.soup)
        rating_5_30 = ParsePlayersStats.get_rating_vs_tops(self.soup)
        maps_5_30 = ParsePlayersStats.get_maps_vs_tops(self.soup)
        kast, impact = ParsePlayersStats.get_kast_and_impact(self.soup)
        age = ParsePlayersStats.get_age(self.soup, 1719608400 - self.current_date)
        self.tmp_data = [name, total_kills, HS, total_deaths, dmg_round, maps_played, rounds_played, kill_round,
                         assist_round, death_round, rating, rating_5_30, maps_5_30, kast, impact, age, ]

    def parse_individual_page(self):
        kills_0_5, open_kills, open_deaths, open_ratio, open_rating, rifle_kills, \
            sniper_kills = ParsePlayersStats.get_data_from_individual_page(self.soup)
        self.tmp_data += [kills_0_5, open_kills, open_deaths, open_ratio, open_rating, rifle_kills, sniper_kills]

    def working_with_variables_assignments(self, _print=True):
        for stat_index, stat_name in enumerate(STATS_NAMES):
            if _print:
                print(stat_index, stat_name, self.tmp_data[stat_index])
            self.player_stats[stat_name] = self.tmp_data[stat_index]
        self.tmp_data = []

    def edit_link(self, prefix):
        if prefix == "overview":
            self.current_link = self.current_link.replace("player/", "stats/players/")
            date = self.current_date
            unix_date_end = date - 24 * 3600
            unix_date_start = date - 24 * 3600 * 91
            str_date_end = datetime.datetime.fromtimestamp(unix_date_end).strftime('%Y-%m-%d')
            str_date_start = datetime.datetime.fromtimestamp(unix_date_start).strftime('%Y-%m-%d')
            self.current_link += f"?startDate={str_date_start}&endDate={str_date_end}"
        else:
            self.current_link = self.current_link.replace("players/", "players/individual/")

    def get_filtered_players_links(self):
        self.filtered_players_links = pickle.load(
            open(f'{con.MAIN_PATH}Data/PlayersStats/filtered_players_links.pkl', "rb"))

    def get_soup(self, prefix):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/PlayersStats/HTML/{prefix}_{self.file_name}.html'):
            self.soup = self.get_player_page(self.current_link)
        else:
            self.soup = self.get_exist_html_file(prefix, self.current_link)

    def get_player_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_teams_matches_pages, verify=False)
        time.sleep(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response, status code:", response.status_code)
            return None

    def get_exist_html_file(self, prefix, link):
        with open(f'{con.MAIN_PATH}Data/PlayersStats/HTML/{prefix}_{self.file_name}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        test_soup = soup.find("div", {"class": "bgPadding"})
        if test_soup is None:
            soup = self.get_player_page(link)

        return soup

    def clear_player_stats(self):
        self.player_stats = {}

    def save_into_pickle_file(self):
        pickle.dump(self.player_stats,
                    open(f'{con.MAIN_PATH}Data/PlayersStats/Stats/{self.file_name}.pkl',
                         "wb"))

    def save_page_into_html(self, soup, prefix):
        with open(f'{con.MAIN_PATH}Data/PlayersStats/HTML/{prefix}_{self.file_name}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))
