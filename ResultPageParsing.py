import datetime
import pickle
import traceback

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import Constants as con

example_dict = {
    "date": [
        {
            "team1": "name1",
            "team2": "name2",
            "score1": 10,
            "score2": 13,
            "stars": 2,
        },
    ]
}


def get_unix_date(date):
    date = date.replace("Results for ", "").strip().split(" ")
    date[0] = str(con.MONTHS_INVERSE[date[0].lower()])
    date[1] = ''.join(filter(str.isdigit, date[1]))

    line = date[2] + " " + date[0] + " " + date[1]
    unix_time = int(datetime.datetime.strptime(line, '%Y %m %d').timestamp() + 3600 * 3)
    return unix_time


class ResultParsing:
    def __init__(self):
        self.main_dict = {}
        self.current_page = 0
        self.start_page = 0
        self.max_page = 150

    def go_every_page(self):
        for self.current_page in tqdm(range(self.start_page, self.max_page)):
            offset = 100 * self.current_page
            soup = self.get_page(offset)
            if soup is not None:
                try:
                    self.save_page_into_html(soup)
                    self.parse_page(soup)
                    self.save_into_pickle_file()
                    self.clear_info_dict()
                except:
                    print(traceback.format_exc())

    def get_page(self, offset):
        params = {
            'offset': offset,
        }

        response = requests.get('https://www.hltv.org/results', params=params, headers=con.headers_for_result_page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            print("Bad response")
            return None

    def parse_page(self, soup):
        days_elements = soup.find_all("div", {"class": "results-sublist"})
        for day_element in days_elements:
            day_line = day_element.find("span", {"class": "standard-headline"}).text
            unix_time = get_unix_date(day_line)
            matches = []
            matches_elements = day_element.find_all("div", {"class": "result-con"})
            for match_element in matches_elements:
                two_team_elements = match_element.find_all("td", {"class": "team-cell"})
                team_1 = two_team_elements[0].text.replace("\n", "")
                team_2 = two_team_elements[1].text.replace("\n", "")
                score_element = match_element.find("td", {"class": "result-score"}).text.replace("\n", "")
                score_element = score_element.replace("- ", "").split()
                stars = match_element.find("div", {"class": "stars"})
                if stars is not None:
                    stars = len(stars.find_all("i"))
                else:
                    stars = 0

                # print(unix_time, team_1, score_element, team_2, stars)
                matches.append({
                    "team1": team_1,
                    "team2": team_2,
                    "score1": score_element[0],
                    "score2": score_element[1],
                    "stars": stars,
                }, )
            self.main_dict[unix_time] = matches

    def clear_info_dict(self):
        self.main_dict = {}

    def save_into_pickle_file(self):
        pickle.dump(self.main_dict,
                    open(f'{con.MAIN_PATH}Data/Results/All/results_page_{self.current_page}.pkl', "wb"))

    def save_page_into_html(self, soup):
        with open(f'{con.MAIN_PATH}Data/Results/HTML/results_page_{self.current_page}.html', "w",
                  encoding="utf-8") as file:
            file.write(str(soup.prettify()))

    def unite_all_pickle_files(self):
        united_dict = {}
        for self.current_page in tqdm(range(self.max_page)):
            current_data = pickle.load(open(f'{con.MAIN_PATH}Data/Results/All/results_page_{self.current_page}.pkl', "rb"))
            united_dict.update(current_data)

        print("keys in dict:", len(united_dict.keys()))
        pickle.dump(united_dict, open(f'{con.MAIN_PATH}Data/Results/All/results_complete.pkl', "wb"))
