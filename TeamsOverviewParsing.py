import datetime
import os
import pickle
import time
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_overview_dict = {
    "teamName_time": {
        "maps_played": 20,
        "wins": 13,
        "loss": 7,
        "kills": 1337,
        "deaths": 1000,
        "rounds_played": 200,
        "k_d": 1.1,
    }
}

example_maps_dict = {
    "teamName_time": [
        {
            "map_name": "",
            "win": "",
            "loss": "",
            "total_rounds": "",
            "open_wins": "",
            "open_loss": "",
        }
    ]
}


class TeamsParsing:
    def __init__(self, parse_overview=True):
        self.all_data = {}
        self.all_matches_data = {}
        self.filtered_matches_data = {}
        self.current_team_name = ""
        self.key_name = ''
        self.current_page = 0
        self.total_teams_count = 0
        self.current_team_num = 0
        self.soup = None
        self.parse_overview = parse_overview
        self.prefix = "overview" if parse_overview else "maps_stats"
        self.folder = "TeamsOverview" if parse_overview else "TeamsMapsStats"

    def go_every_team(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()

        for self.key_name in tqdm(list(self.filtered_matches_data.keys())):
            self.current_team_name = self.key_name[:self.key_name.find("_")]
            link = self.prepare_link()
            self.get_soup(link)

            if self.soup is not None:
                try:
                    if self.parse_overview:
                        self.parse_overview_page()
                    else:

                        self.parse_maps_page()
                    self.save_into_pickle_file()
                    self.save_page_into_html(soup=self.soup)
                    self.clear_info_dict()
                except:
                    print(link)
                    print(traceback.format_exc())
            self.current_page += 1

    def parse_maps_page(self):
        maps_stats = []
        maps_indexes = self.get_maps_indexes()
        for map_index in maps_indexes:
            map_name, win, loss, total_rounds, open_wins, open_loss = self.get_all_maps_stats(map_index)
            maps_stats.append([map_name, win, loss, total_rounds, open_wins, open_loss])

        key_for_dict = str(self.current_team_name + "_" + str(self.filtered_matches_data[self.key_name][1]))
        self.all_data[key_for_dict] = maps_stats
        # print(self.all_data)

    def get_all_maps_stats(self, map_index):
        vals_list = []
        if map_index != -1:
            all_maps_elements = self.soup.find("div", {"class": "two-grid"})

            map_name = all_maps_elements.find_all("div", {"class": "map-pool-map-name"})[map_index]
            map_name = map_name.text.replace("\n", "").strip()
            vals_list.append(map_name)

            map_stat_element = all_maps_elements.find_all("div", {"class": 'stats-rows standard-box'})[map_index]
            stats_elements = map_stat_element.find_all("div", {"class": "stats-row"})
            stats_values = [value.find_all("span")[1].text.replace("\n", "").strip() for value in stats_elements]
            stats_values = [value.replace("%", "").replace(" /", "") for value in stats_values]

            for value_index, value in enumerate(stats_values):
                if value_index == 0:
                    split_values = value.split(" ")
                    wins = int(split_values[0])
                    loss = int(split_values[2])
                    vals_list += [wins, loss]
                elif value_index == 1:
                    continue
                elif value_index == 2:
                    vals_list.append(int(value))
                else:
                    vals_list.append(float(value))

            return vals_list
        return [None, None, None, None, None, None]

    def get_maps_indexes(self):
        maps_indexes = []
        maps_names_elements = self.soup.find("div", {"class": "two-grid"}).find_all("div",
                                                                                    {"class": "map-pool-map-name"})
        maps_names = [map_element.text.replace("\n", "").strip() for map_element in maps_names_elements]
        for map_name in self.filtered_matches_data[self.key_name][2]:
            if map_name in maps_names:
                current_map_index = maps_names.index(map_name)
                maps_indexes.append(current_map_index)
            else:
                maps_indexes.append(-1)
        return maps_indexes

    def parse_overview_page(self):
        key_for_dict = str(self.current_team_name + "_" + str(self.filtered_matches_data[self.key_name][1]))
        maps_played, wins, loss, kills, deaths, rounds_played, k_d = self.get_all_overview_values()
        self.all_data[key_for_dict] = {
            "maps_played": maps_played,
            "wins": wins,
            "loss": loss,
            "kills": kills,
            "deaths": deaths,
            "rounds_played": rounds_played,
            "k_d": k_d,
        }
        # print(self.all_data)

    def get_all_overview_values(self):
        vals_list = []
        vals_elements = self.soup.find_all("div", {"class": "col standard-box big-padding"})
        for value_index, value in enumerate(vals_elements):
            if value_index == 0:
                tmp_value = ''.join(filter(str.isdigit, value.text)).replace("\n", "").strip()
                if tmp_value == "0":
                    vals_list = [None, None, None, None, None, None, None]
                    return vals_list
            if value_index == 1:
                split_values = value.text.replace("\n", "").strip().split(" / ")
                wins = int(split_values[0])
                loss = int(split_values[2].lower().replace("wins", ""))
                vals_list += [wins, loss]
            elif value_index == 5:
                vals_list.append(float(value.text.replace("K/D Ratio", "").replace("\n", "").replace(" ", "").strip()))
            else:
                vals_list.append(int(''.join(filter(str.isdigit, value.text))))
        return vals_list

    def prepare_link(self):
        link = self.filtered_matches_data[self.key_name][0]
        link = link.replace("https://www.hltv.org/team", "https://www.hltv.org/stats/teams")
        if not self.parse_overview:
            link = link.replace("teams", "teams/maps")
        unix_date_end = self.filtered_matches_data[self.key_name][1] - 24 * 3600
        unix_date_start = self.filtered_matches_data[self.key_name][1] - 24 * 3600 * 91
        str_date_end = datetime.datetime.fromtimestamp(unix_date_end).strftime('%Y-%m-%d')
        str_date_start = datetime.datetime.fromtimestamp(unix_date_start).strftime('%Y-%m-%d')
        link += f"?startDate={str_date_start}&endDate={str_date_end}"
        return link

    def get_soup(self, link):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/{self.folder}/HTML/team_{self.prefix}_{self.current_page}.html'):
            self.soup = self.get_match_page(link)
        else:
            self.soup = self.get_exist_html_file(link)

    def get_match_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_tournaments_stats)
        time.sleep(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_exist_html_file(self, link):
        with open(f'{con.MAIN_PATH}Data/{self.folder}/HTML/team_{self.prefix}_{self.current_page}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        test_soup = soup.find("div", {"class": "bgPadding"})
        if test_soup is None:
            soup = self.get_match_page(link)

        return soup

    def filter_all_matches_data(self):
        keys = []
        for match in self.all_matches_data.values():
            if f'{match["team1"]}_{match["date"]}' not in keys:
                self.filtered_matches_data[f'{match["team1"]}_{match["date"]}'] = [match["team1_link"], match["date"], match["maps"]]
                keys.append(f'{match["team1"]}_{match["date"]}')
            if f'{match["team2"]}_{match["date"]}' not in keys:
                self.filtered_matches_data[f'{match["team2"]}_{match["date"]}'] = [match["team2_link"], match["date"], match["maps"]]
                keys.append(f'{match["team2"]}_{match["date"]}')

    def get_all_matches_data(self):
        self.all_matches_data = pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

    def clear_info_dict(self):
        self.all_data = {}

    def save_into_pickle_file(self):
        pickle.dump(self.all_data,
                    open(f'{con.MAIN_PATH}Data/{self.folder}/Stats/team_{self.prefix}_{self.current_page}.pkl',
                         "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/{self.folder}/HTML/team_{self.prefix}_{self.current_page}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))

    def unite_all_pickle_files(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()
        self.total_teams_count = len(self.filtered_matches_data)

        united_dict = {}
        for self.current_team_num in tqdm(range(self.total_teams_count)):
            path = f'{con.MAIN_PATH}Data/{self.folder}/Stats/team_{self.prefix}_{self.current_team_num}.pkl'
            if os.path.exists(path):
                current_data = pickle.load(open(path, "rb"))
                # print(current_data)
                united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/{self.folder}/Stats/team_{self.prefix}_complete.pkl', "wb"))
