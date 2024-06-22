import os
import pickle
import time
import datetime

from tqdm import tqdm

import FilteringResultsByRank
import MatchsPagesParsing
import ResultPageParsing
from RankingParsing import RankingParsing
import Constants as con

if __name__ == "__main__":
    # print(datetime.datetime.strptime("2024-06-20", format).timestamp() + 3600 * 3)
    # print(pickle.load(open(f'{con.MAIN_PATH}Data/Ranking/ranking_stats_week_{1}.pkl', "rb")))

    # RankingParsing().go_every_week()
    # RankingParsing().unite_all_pickle_files()
    # ResultPageParsing.ResultParsing().go_every_page()
    # ResultPageParsing.ResultParsing().unite_all_pickle_files()
    # FilteringResultsByRank.FilteringByRank().filter()
    # MatchsPagesParsing.MatchesPages().go_every_match()
    MatchsPagesParsing.MatchesPages().unite_all_pickle_files()

    # print(int(time.time()))
    # current_week_day = datetime.datetime.now().weekday()
    # print((datetime.datetime.now()).weekday())
    # print()
    # print(time.localtime(1718582400))
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1718582400)))
    # print(time.strftime('%Y', time.localtime(1718582400)))
    # print(time.strftime('%m', time.localtime(1718582400)))
    # print(time.strftime('%d', time.localtime(1718582400)))
