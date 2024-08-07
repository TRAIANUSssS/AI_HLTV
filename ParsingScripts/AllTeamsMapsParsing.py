import datetime
import os
import pickle
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_dict = {
    "team_name": {
        "all_played_dates": [1719156775],
        "all_played_maps":
            [
                {
                    "date": 1719156775,
                    "opponent": "name",
                    "tournament_name": "tour_name",
                    "map_name": "name",
                    "score1": 13,
                    "score2": 4,
                    "match_link": 'link',
                    "is_first_map": False,
                    "is_first_match": True,
                }
            ]
    }
}


def get_match_data(match_element):
    data = match_element.find("td", {"class": "time"}).find("a").text.replace("\n", "").replace(" ", "")
    unix_time = int(datetime.datetime.strptime(data, '%d/%m/%y').timestamp() + 3600 * 3)
    return unix_time


def get_tournament_name(match_element):
    name = match_element.find("td", {"class": "gtSmartphone-only"}).find("span").text.replace("\n", "").strip()
    return name


def get_opponent_name(match_element):
    name = match_element.find_all("td")[3].text.replace("\n", "").strip()
    return name


def get_map_name(match_element):
    map_name = match_element.find("td", {"class": "statsMapPlayed"}).text.replace("\n", "").replace(" ", "")
    return map_name


def get_score(match_element):
    score = match_element.find("span", {"class": "statsDetail"}).text.replace("\n", "")
    score = score.replace(" ", "").split("-")
    return score[0], score[1]


def get_match_link(match_element):
    link = "https://www.hltv.org" + match_element.find("td", {"class": "time"}).find("a").get("href")
    return link


class TeamsMatchesParsing:
    def __init__(self):
        self.all_teams_matches_data = {}
        self.all_matches_data = {}
        self.filtered_matches_data = {}
        self.current_team_name = ""
        self.current_match_num = 0
        self.soup = None
        self.current_team_num = 0
        self.total_teams_count = 0

    def go_every_team(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()

        for self.current_team_name in tqdm(list(self.filtered_matches_data.keys())):
            self.get_soup()

            if self.soup is not None:
                try:
                    self.parse_matches_pages()
                    self.add_is_first_match_map()
                    self.save_into_pickle_file()
                    self.save_page_into_html(self.soup)
                    self.clear_info_dict()
                except:
                    print(self.filtered_matches_data[self.current_team_name])
                    print(traceback.format_exc())

            self.current_match_num += 1

    def parse_matches_pages(self):
        all_matches_elements = self.soup.find("tbody").find_all("tr")
        all_played_dates = []
        all_played_maps = []

        for match_element in all_matches_elements:
            map_name = get_map_name(match_element)
            if map_name not in con.MAP_POOL:
                continue
            date = get_match_data(match_element)
            if date < 1648684800:
                continue
            tournament_name = get_tournament_name(match_element)
            opponent_name = get_opponent_name(match_element)
            score1, score2 = get_score(match_element)
            match_link = get_match_link(match_element)

            match_data = {
                "date": date,
                "opponent": opponent_name,
                "tournament_name": tournament_name,
                "map_name": map_name,
                "score1": score1,
                "score2": score2,
                "match_link": match_link,
            }
            all_played_maps.append(match_data)
            all_played_dates.append(date)

        self.all_teams_matches_data[self.current_team_name] = {
            "all_played_dates": all_played_dates,
            "all_played_maps": all_played_maps,
        }
        # print(self.all_teams_matches_data)

    def add_is_first_match_map(self):
        all_tours = {}
        tmp_all_matches_data = []
        reversed_all_matches_data = list(self.all_teams_matches_data.values())[0]["all_played_maps"][::-1]
        prev_tour = reversed_all_matches_data[0]["tournament_name"]
        prev_opponent = reversed_all_matches_data[0]["opponent"]
        is_first_match = True

        for val in reversed_all_matches_data:
            all_tours[val["tournament_name"]] = False

        tmp_match = reversed_all_matches_data[0]
        tmp_match["is_first_map"] = True
        tmp_match["is_first_match"] = True
        all_tours[reversed_all_matches_data[0]["tournament_name"]] = True
        tmp_all_matches_data.append(tmp_match)

        for match in reversed_all_matches_data[1:]:
            curr_tour = match["tournament_name"]
            curr_opponent = match["opponent"]
            is_first_map = prev_tour != curr_tour
            is_first_match = False if prev_tour != curr_tour else is_first_match
            is_first_match = True if is_first_map and not all_tours[curr_tour] else is_first_match
            is_first_match = False if prev_opponent != curr_opponent and not is_first_map else is_first_match
            tmp_match = match
            tmp_match["is_first_map"] = is_first_map
            tmp_match["is_first_match"] = is_first_match
            tmp_all_matches_data.append(tmp_match)
            prev_opponent = curr_opponent
            prev_tour = curr_tour
            all_tours[curr_tour] = True
        self.all_teams_matches_data[self.current_team_name]["all_played_maps"] = tmp_all_matches_data[::-1]


    def get_soup(self):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/TeamsMaps/HTML/team_matches_page_{self.current_match_num}.html'):
            self.soup = self.get_match_page(self.filtered_matches_data[self.current_team_name])
        else:
            self.soup = self.get_exist_html_file()

    def get_match_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_teams_matches_pages)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_exist_html_file(self):
        with open(f'{con.MAIN_PATH}Data/TeamsMaps/HTML/team_matches_page_{self.current_match_num}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def filter_all_matches_data(self):
        keys = []
        for match in self.all_matches_data.values():
            if match["team1"] not in keys:
                self.filtered_matches_data[match["team1"]] = match["team1_link"].replace(
                    "https://www.hltv.org/team", "https://www.hltv.org/stats/teams/matches")
                keys.append(match["team1"])
            if match["team2"] not in keys:
                self.filtered_matches_data[match["team2"]] = match["team2_link"].replace(
                    "https://www.hltv.org/team", "https://www.hltv.org/stats/teams/matches")
                keys.append(match["team2"])

    def get_all_matches_data(self):
        self.all_matches_data = pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

    def clear_info_dict(self):
        self.all_teams_matches_data = {}

    def save_into_pickle_file(self):
        pickle.dump(self.all_teams_matches_data,
                    open(f'{con.MAIN_PATH}Data/TeamsMaps/Pages/team_matches_page_{self.current_match_num}.pkl', "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/TeamsMaps/HTML/team_matches_page_{self.current_match_num}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))

    def unite_all_pickle_files(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()
        self.total_teams_count = len(self.filtered_matches_data)

        united_dict = {}
        for self.current_team_num in tqdm(range(self.total_teams_count)):
            path = f'{con.MAIN_PATH}Data/TeamsMaps/Pages/team_matches_page_{self.current_team_num}.pkl'
            if os.path.exists(path):
                current_data = pickle.load(open(path, "rb"))
                united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/TeamsMaps/Pages/match_complete.pkl', "wb"))
