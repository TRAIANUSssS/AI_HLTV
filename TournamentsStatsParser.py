import datetime
import os
import pickle
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_dict = {
    "link": {
        "tour_name": "name",
        "prize_pool": 200000,
        "for_invite": False,
        "is_lan": True,
        "start_date": 1718150400,
        "tour_type": 1,
    }
}


class TournamentsStatsParsing:
    def __init__(self):
        self.all_matches_data = {}
        self.filtered_tours_data = []
        self.all_tours_data = {}
        self.current_tour_num = 0
        self.total_tours_count = 0
        self.soup = None

    def go_every_tournament(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()

        for self.current_tour_num in tqdm(range(len(self.filtered_tours_data))):
            self.get_soup()

            if self.soup is not None:
                try:
                    self.parse_tour_page()
                    self.save_into_pickle_file()
                    self.save_page_into_html(self.soup)
                    self.clear_info_dict()
                except:
                    print(self.filtered_tours_data[self.current_tour_num])
                    print(traceback.format_exc())

    def parse_tour_page(self):
        tour_name = self.get_tour_name()
        prize_pool, for_invite = self.get_prize_pool()
        is_lan = self.get_is_lan()
        start_date = self.get_start_date()
        tour_type = 2 if tour_name.lower().count("major") else 1 if prize_pool >= 200000 else 0
        # print(tour_name, prize_pool, for_invite, is_lan, start_date, tour_type,
        #       self.filtered_tours_data[self.current_tour_num])
        self.all_tours_data[self.filtered_tours_data[self.current_tour_num]] = {
            "tour_name": tour_name,
            "prize_pool": prize_pool,
            "for_invite": for_invite,
            "is_lan": is_lan,
            "start_date": start_date,
            "tour_type": tour_type,
        }

    def get_tour_name(self):
        name = self.soup.find("h1").text.replace("\n", "").strip()
        return name

    def get_prize_pool(self):
        prize_pool_line = self.soup.find("td", {"class": "prizepool text-ellipsis"}).text.replace("\n", "").strip()
        money = ''.join(filter(str.isdigit, prize_pool_line))
        for_invite = len(prize_pool_line) - len(money) > 7
        money = int(money) if money != "" else 0
        return money, for_invite

    def get_is_lan(self):
        location = self.soup.find("td", {"location gtSmartphone-only"}).text.replace("\n", "").strip()
        is_lan = False if location.count("Online") else True
        return is_lan

    def get_start_date(self):
        date_line = self.soup.find("td", {"class": "eventdate"}).text.replace("\n", "").strip()
        date_list = date_line.split(" ")
        date_line = ''.join(filter(str.isdigit, date_list[1])) + " " + \
                    str(con.MONTHS_INVERSE[date_list[0].lower()]) + " " + \
                    date_list[-1]
        unix_time = int(datetime.datetime.strptime(date_line, '%d %m %Y').timestamp() + 3600 * 3)
        return unix_time

    def filter_all_matches_data(self):
        keys = []
        for match in self.all_matches_data.values():
            if match["tournament_link"] not in keys:
                self.filtered_tours_data.append(match["tournament_link"])
                keys.append(match["tournament_link"])
        # print(len(keys))

    def get_soup(self):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/TournamentsStats/HTML/tour_page_{self.current_tour_num}.html'):
            self.soup = self.get_match_page(self.filtered_tours_data[self.current_tour_num])
        else:
            self.soup = self.get_exist_html_file()

    def get_match_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_tournaments_stats)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_exist_html_file(self):
        with open(f'{con.MAIN_PATH}Data/TournamentsStats/HTML/tour_page_{self.current_tour_num}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        return soup

    def get_all_matches_data(self):
        self.all_matches_data = pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb"))

    def clear_info_dict(self):
        self.all_tours_data = {}

    def save_into_pickle_file(self):
        pickle.dump(self.all_tours_data,
                    open(f'{con.MAIN_PATH}Data/TournamentsStats/Stats/tour_page_{self.current_tour_num}.pkl',
                         "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/TournamentsStats/HTML/tour_page_{self.current_tour_num}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))

    def unite_all_pickle_files(self):
        self.get_all_matches_data()
        self.filter_all_matches_data()
        self.total_tours_count = len(self.filtered_tours_data)

        united_dict = {}
        for self.current_tour_num in tqdm(range(self.total_tours_count)):
            path = f'{con.MAIN_PATH}Data/TournamentsStats/Stats/tour_page_{self.current_tour_num}.pkl'
            if os.path.exists(path):
                current_data = pickle.load(open(path, "rb"))
                united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/TournamentsStats/Stats/tours_complete.pkl', "wb"))
