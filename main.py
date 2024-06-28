import os
import pickle
import time
import datetime

from tqdm import tqdm

import AllTeamsMapsParsing
import FilteringResultsByRank
import GetLinksToMatches
import MatchsPagesParsing
import ResultPageParsing
import TeamsOverviewParsing
import TournamentsStatsParser
from RankingParsing import RankingParsing
import Constants as con

if __name__ == "__main__":
    # print(time.time())
    # print(datetime.datetime.strptime("2024-06-20", format).timestamp() + 3600 * 3)
    # print(datetime.datetime.fromtimestamp(1718622000).strftime('%Y-%m-%d'))
    # print(pickle.load(open(f'{con.MAIN_PATH}Data/TeamsOverview/Stats/team_overview_complete.pkl', "rb")))
    # [print(value) for value in pickle.load(open(f'{con.MAIN_PATH}Data/Matches/MatchesData/match_complete.pkl', "rb")).values()]
    # print(1682743800 - (1682743800 % 86400))
    # date = pickle.load(open(f'{con.MAIN_PATH}Data/TeamsMaps/Pages/team_matches_page_1.pkl', "rb"))
    # for val in list(date["3DMAX"]["all_played_maps"]):
    #     print(val["opponent"], val["tournament_name"], val["map_name"], val["is_first_map"], val["is_first_match"], val["date"],)


    # RankingParsing().go_every_week()
    # RankingParsing().unite_all_pickle_files()
    # ResultPageParsing.ResultParsing().go_every_page()
    # ResultPageParsing.ResultParsing().unite_all_pickle_files()
    # FilteringResultsByRank.FilteringByRank().filter()
    # MatchsPagesParsing.MatchesPages().go_every_match()
    # MatchsPagesParsing.MatchesPages().unite_all_pickle_files()
    # AllTeamsMapsParsing.TeamsMatchesParsing().go_every_team()
    # AllTeamsMapsParsing.TeamsMatchesParsing().unite_all_pickle_files()
    # TournamentsStatsParser.TournamentsStatsParsing().go_every_tournament()
    # TournamentsStatsParser.TournamentsStatsParsing().unite_all_pickle_files()
    # TeamsOverviewParsing.TeamsParsing(True).go_every_team()
    # TeamsOverviewParsing.TeamsParsing(True).unite_all_pickle_files()
    # TeamsOverviewParsing.TeamsParsing(False).go_every_team()
    # TeamsOverviewParsing.TeamsParsing(False).unite_all_pickle_files()
    GetLinksToMatches.GetLinks().get_links()

    # print(int(time.time()))
    # current_week_day = datetime.datetime.now().weekday()
    # print((datetime.datetime.now()).weekday())
    # print()
    # print(time.localtime(1718582400))
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1718582400)))
    # print(time.strftime('%Y', time.localtime(1718582400)))
    # print(time.strftime('%m', time.localtime(1718582400)))
    # print(time.strftime('%d', time.localtime(1718582400)))
