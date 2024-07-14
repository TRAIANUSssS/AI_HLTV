import datetime
import os
import pickle
import time
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con


def get_all_players_links():
    return pickle.load(open(f'{con.MAIN_PATH}Data/PlayersStats/all_players_links.pkl', "rb"))


class GetPlayersTeamsData:
    def __init__(self):
        self.all_players_links = get_all_players_links()
        self.all_players_teams = {}
        self.soup = None
        self.link = ""
        self.player_name = ""

    def go_every_link(self):
        # for self.link in self.all_players_links:
        for self.link in tqdm(self.all_players_links):
            self.player_name = self.link.split("/")[-1]
            self.edit_link()
            self.get_soup()
            if self.soup is not None:
                try:
                    self.parse_page()
                    self.save_into_pickle_file()
                    self.save_page_into_html(self.soup)
                    self.clear_player_all_teams_data()
                except:
                    print(self.link)
                    print(traceback.format_exc())

    def parse_page(self):
        self.all_players_teams = {
            "all_dates": []
        }
        all_matches = self.soup.find("tbody").find_all("tr")
        last_team = ""
        for match_data in all_matches[::-1]:
            current_team = match_data.find("span").text.replace("\n", "").replace(" ", "")
            if current_team != last_team:
                date = int(match_data.find("div", {"class": "time"}).get("data-unix")) // 1000
                self.all_players_teams["all_dates"].append(date)
                self.all_players_teams[date] = current_team
                last_team = current_team
        # print(self.all_players_teams)


    def edit_link(self):
        self.link = self.link.replace("https://www.hltv.org/player/", "https://www.hltv.org/stats/players/matches/")

    def get_soup(self):
        if not os.path.exists(
                f'{con.MAIN_PATH}Data/PlayersStats/HTML/all_maps_{self.player_name}.html'):
            self.soup = self.get_player_page(self.link)
        else:
            self.soup = self.get_exist_html_file(self.link)

    def get_player_page(self, link):
        con.headers_for_teams_matches_pages["Referer"] = link
        response = requests.get(link, headers=con.headers_for_teams_matches_pages)
        time.sleep(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_exist_html_file(self, link):
        with open(f'{con.MAIN_PATH}Data/PlayersStats/HTML/all_maps_{self.player_name}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        test_soup = soup.find("div", {"class": "bgPadding"})
        if test_soup is None:
            soup = self.get_player_page(link)

        return soup

    def clear_player_all_teams_data(self):
        self.all_players_teams = {}

    def save_into_pickle_file(self):
        pickle.dump(self.all_players_teams,
                    open(f'{con.MAIN_PATH}Data/PlayersStats/AllMatches/all_maps_{self.player_name}.pkl',
                         "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/PlayersStats/HTML/all_maps_{self.player_name}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))
