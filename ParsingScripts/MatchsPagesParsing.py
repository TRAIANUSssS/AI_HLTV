import os
import pickle
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_dict = {
    "id_MatchName": {
        "date": 1718150400,
        "is_grand_final": True,
        "team1": "name1",
        "team2": "name2",
        "maps_count": 3,
        "maps": ["Dust2", "Nuke", "Inferno"],
        "who_picked": [1, 2, 1],
        "tournament_link": "link",
        "team1_link": "link",
        "team2_link": "link",
        "players": ["p11", "p12", "p13", "p14", "p15", "p21", "p22", "p23", "p24", "p25"],
        "players_links": {
            "p11": "link",
            # ...
            "p25": "link",
        },
        "days_in_team": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    }
}


class MatchesPages:
    def __init__(self):
        self.matches_data = {}
        self.results_data = {}
        self.all_matches_list = []
        self.soup = None
        self.current_match_num = 0
        self.total_matches = len(self.all_matches_list)

    def go_every_match(self):
        self.get_results_data()
        self.edit_results_data()

        self.current_match_num = 0
        for match_data in tqdm(self.all_matches_list):
            if match_data["link"].count("showmatch"):
                self.current_match_num += 1
                continue

            if not os.path.exists(f'{con.MAIN_PATH}Data/Matches/HTML/match_page_{self.current_match_num}.html'):
                self.soup = self.get_match_page(match_data["link"])
            else:
                self.soup = self.get_exist_html_file(match_data["link"])

            if self.soup is not None:
                try:
                    self.save_page_into_html(self.soup)
                    match_id = self.get_match_id(match_data["link"])
                    result = self.parse_match_page(match_id)
                    if result:
                        self.save_into_pickle_file()
                    self.clear_info_dict()
                except:
                    print(match_data["link"])
                    print(traceback.format_exc())
            self.current_match_num += 1

    def get_match_page(self, link):
        response = requests.get(link, headers=con.headers_for_match_page, )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def get_exist_html_file(self, link):
        with open(f'{con.MAIN_PATH}Data/Matches/HTML/match_page_{self.current_match_num}.html', "r",
                  encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        test_soup = soup.find("div", {"class": "bgPadding"})

        if test_soup is None:
            soup = self.get_match_page(link)

        return soup

    def get_match_id(self, link):
        match_id = link.replace("https://www.hltv.org/matches/", "").replace("/", "_")
        return match_id

    def parse_match_page(self, match_id):
        is_bad_match = self.check_match()
        if is_bad_match:
            return False
        maps_count, is_grand_final = self.get_maps_count_and_is_grand_final()
        team1_name, team2_name = self.get_teams_names()
        maps_list, who_picked = self.get_maps_and_veto(team1_name)

        tournament_link = self.get_tournament_link()
        team1_link, team2_link = self.get_teams_links()
        players, players_links = self.get_players_and_links(team1_name)
        date = self.get_match_date()

        # print(date, is_grand_final, maps_count, team1_name, team2_name, maps_list, who_picked, tournament_link,
        #       team1_link, team2_link, players, players_links)
        self.matches_data[match_id] = {
            "date": date,
            "is_grand_final": is_grand_final,
            "team1": team1_name,
            "team2": team2_name,
            "maps_count": maps_count,
            "maps": maps_list,
            "who_picked": who_picked,
            "tournament_link": tournament_link,
            "team1_link": team1_link,
            "team2_link": team2_link,
            "players": players,
            "players_links": players_links
        }
        return True

    def get_match_date(self):
        date = self.soup.find("div", {"class": "date"}).get("data-unix")
        date = int(date) // 1000
        return date

    def get_players_and_links(self, team1_name):
        players = []
        players_links = {}
        players_stats_element = self.soup.find("div", {"id": "all-content"}).find_all("table",
                                                                                      {"class": "table totalstats"})

        first_team_players_elements = players_stats_element[0]
        if not first_team_players_elements.text.count(team1_name):
            first_team_players_elements = players_stats_element[1]
            second_team_players_elements = players_stats_element[0]
        else:
            second_team_players_elements = players_stats_element[1]

        players_stats_element = [first_team_players_elements, second_team_players_elements]
        for team_element in players_stats_element:
            players_elements = team_element.find_all("td", {"class": "players"})[1:]
            for player_element in players_elements:
                nick = player_element.find("span", {"class": "player-nick"}).text.replace("\n", "").strip()
                link = "https://www.hltv.org" + player_element.find("a").get("href")
                players.append(nick)
                players_links[nick] = link

        return players, players_links

    def get_teams_links(self):
        teams_elements = self.soup.find_all("div", {"class": "team"})
        team1_link = "https://www.hltv.org" + teams_elements[0].find("a").get("href")
        team2_link = "https://www.hltv.org" + teams_elements[1].find("a").get("href")
        return team1_link, team2_link

    def get_tournament_link(self):
        tournament_link_element = self.soup.find("div", {"class": "event text-ellipsis"}).find("a")
        tournament_link = "https://www.hltv.org" + tournament_link_element.get("href")
        return tournament_link

    def get_maps_and_veto(self, team1_name):
        maps_list = []
        who_picked = []
        maps_veto_elements = self.soup.find_all("div", {"standard-box veto-box"})[1].find("div", {
            "class": "padding"}).find_all("div")
        for map_veto in maps_veto_elements:
            veto_line = map_veto.text
            if veto_line.count("picked"):
                maps_list.append(veto_line.split()[-1])
                who_picked.append(0 if veto_line.count(team1_name) else 1)
            if veto_line.count("left"):
                maps_list.append(veto_line.split()[1])
                who_picked.append(0)
        return maps_list, who_picked

    def get_teams_names(self, ):
        teams_names_elements = self.soup.find("div", {"class": "standard-box teamsBox"}).find_all("div",
                                                                                                  {"class": "teamName"})
        team1_name = teams_names_elements[0].text.replace("\n", "").strip()
        team2_name = teams_names_elements[1].text.replace("\n", "").strip()
        return team1_name, team2_name

    def get_maps_count_and_is_grand_final(self, ):
        is_grand_final_element = self.soup.find("div", {"class": "padding preformatted-text"}).text
        is_grand_final = bool(is_grand_final_element.lower().count("grand final"))
        maps_count = int(is_grand_final_element.strip().replace("Best of ", "")[0])
        return maps_count, is_grand_final

    def check_match(self):
        def_map = self.soup.find("div", {"class": "mapname"}).text.strip()
        return def_map == "Default"

    def edit_results_data(self):
        for day_data in self.results_data.values():
            self.all_matches_list += day_data

    def clear_info_dict(self):
        self.matches_data = {}

    def get_results_data(self):
        self.results_data = pickle.load(open(f'{con.MAIN_PATH}Data/Results/All/results_complete_filtered.pkl', "rb"))

    def save_into_pickle_file(self):
        pickle.dump(self.matches_data,
                    open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_page_{self.current_match_num}.pkl', "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/Matches/HTML/match_page_{self.current_match_num}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))

    def unite_all_pickle_files(self):
        self.get_results_data()
        self.edit_results_data()
        self.total_matches = len(self.all_matches_list)

        united_dict = {}
        for self.current_match_num in tqdm(range(self.total_matches)):
            path = f'{con.MAIN_PATH}Data/Matches/MatchesData/match_page_{self.current_match_num}.pkl'
            if os.path.exists(path):
                current_data = pickle.load(open(path, "rb"))
                if "date" in list(current_data.values())[0].keys():
                    united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "wb"))
