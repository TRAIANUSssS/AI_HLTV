import os
import pickle

import Constants as con


def edit_players_stats_files():
    files = os.listdir(f'{con.MAIN_PATH}Data/PlayersStats/Stats')
    for file in files:
        if file.count(" ") or file.count("-") or file.count("Š") or file.count("ś") or file.count("ó") or file.count("ı") or file.count("_"):
            data = pickle.load(open(f'{con.MAIN_PATH}Data/PlayersStats/Stats/{file}', "rb"))
            old_file_name = file
            file = file.replace("-", "")
            file = file.replace(" ", "").replace("Š", "").replace("ś", "").replace("ó", "")
            file = file.replace("_", "").replace("ı", "")
            pickle.dump(data, open(f'{con.MAIN_PATH}Data/PlayersStats/Stats/{file}', "wb"))
            os.remove(f'{con.MAIN_PATH}Data/PlayersStats/Stats/{old_file_name}')
            print(file)
