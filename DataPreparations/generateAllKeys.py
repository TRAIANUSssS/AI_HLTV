def gen_all_keys():
    match_list = ["is_grand_final", "maps_count", "who_picked", "stars"]
    tournament_list = ["prize_pool", "for_invite", "is_lan", "start_date", "tour_type"]
    team_overview_list = get_team_overview()  # count: 14
    maps_stats_list = gen_maps_keys()  # count: 60
    last_5_matches_list = gen_last_5_matches_keys()  # count: 7790
    players_stats_list = get_players_stats_list()  # count: 330

    ALL_KEYS = match_list + \
               tournament_list + \
               team_overview_list + \
               maps_stats_list + \
               last_5_matches_list + \
               players_stats_list
    print(len(ALL_KEYS))
    return ALL_KEYS


def get_team_overview():
    team_overview_base_list = ["maps_played", "wins", "loss", "kills", "deaths", "rounds_played", "k_d", ]
    team_overview_list = []
    for team_index in range(2):
        for stat_index in range(len(team_overview_base_list)):
            line = f"team{team_index}_{team_overview_base_list[stat_index]}"
            team_overview_list.append(line)
    return team_overview_list


def gen_maps_keys():
    maps_stats_base_list = ["map_type", "win", "loss", "total_rounds", "open_wins", "open_loss", ]
    maps_stats_list = []
    for team_index in range(2):
        for map_index in range(5):
            for stat_index in range(6):
                line = f"team{team_index}_map{map_index}_{maps_stats_base_list[stat_index]}"
                maps_stats_list.append(line)
    return maps_stats_list


def gen_last_5_matches_keys():
    last_5_matches_base_list = ["rank_1", "rank_2", "points1", "points2", "map_name", "score1", "score2",
                                "first_side_score1", "first_side_score2", "second_side_score1", "second_side_score2",
                                "rating1", "rating2", "first_kills1", "first_kills2", "clutches_won1", "clutches_won2",
                                "round_winners", "round_history", "players_stats"]
    last_5_matches_players_stats_names = ["kills", "assist", "deaths", "kast", "kd_diff", "adr", "FK", "rating", ]
    last_5_matches_list = []
    for team_index in range(2):
        for map_index in range(19):
            for stat_index in range(len(last_5_matches_base_list)):
                line = f"team{team_index}_map{map_index}_{last_5_matches_base_list[stat_index]}"
                if stat_index < 17:
                    last_5_matches_list.append(line)
                elif 17 <= stat_index <= 18:
                    for round_index in range(54):
                        line = f"{line}_round{round_index}"
                        last_5_matches_list.append(line)
                else:
                    for player_index in range(10):
                        for player_stat_index in range(len(last_5_matches_players_stats_names)):
                            line = f"{line}_player{player_index}_{last_5_matches_players_stats_names[player_stat_index]}"
                            last_5_matches_list.append(line)
    return last_5_matches_list


def get_players_stats_list():
    players_stat_base_list = ["total_kills", "HS", "total_deaths", "dmg_round", "maps_played", "rounds_played",
                              "kill_round", "assist_round", "death_round", "rating", "kast", "impact", "age",
                              "open_kills", "open_deaths", "open_ratio", "open_rating", "rifle_kills", "sniper_kills",
                              "rating_5_30", "maps_5_30", "kills_0_5"]
    players_stat_list = []
    for player_index in range(10):
        for stat_index in range(len(players_stat_base_list)):
            line = f"player{player_index}_{players_stat_base_list[stat_index]}"
            if stat_index < 19:
                players_stat_list.append(line)
            elif 19 <= stat_index <= 21:
                need_iterations = 6 if stat_index == 21 else 4
                for additional_index in range(need_iterations):
                    line = f"{line}_{additional_index}"
                    players_stat_list.append(line)
    return players_stat_list
