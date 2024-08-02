def get_date(soup):
    date = soup.find("span", {"data-time-format": "yyyy-MM-dd HH:mm"}).get("data-unix")
    date = int(date) // 1000
    return date


def get_teams_names(soup):
    teams_names_list = soup.find_all("a", {"class": "block text-ellipsis"})[1:]
    teams_names_list = [team_element.text.replace("\n", "").strip() for team_element in teams_names_list]
    return teams_names_list


def get_map_name(soup):
    map_element = soup.find("div", {"class": "match-info-box"})
    link_text = map_element.find("a").text
    first_div = map_element.find("div").text
    map_name = map_element.text.replace(link_text, "").replace(first_div, "").replace("\n", "").strip()
    map_name = map_name[:map_name.find(" ")]
    return map_name


def get_score(soup):
    score_1 = soup.find("div", {"team-left"}).find("div").text.replace("\n", "").strip()
    score_2 = soup.find("div", {"team-right"}).find("div").text.replace("\n", "").strip()
    return int(score_1), int(score_2)


def get_side_scors(soup):
    score_element = soup.find("div", {"class": "match-info-row"}).find("div", {"class": "right"})
    score_element = score_element.find_all("span")
    score_element = [elem.text.replace("\n", "").strip() for elem in score_element]
    return score_element[2:]


def get_rating(soup):
    rating_element = soup.find_all("div", {"class": "match-info-row"})[1].find("div", {"class": "right"}).text
    rating_element = rating_element.replace("\n", "").strip().replace(" :", "").split(" ")
    return rating_element


def get_first_kills(soup):
    kills_elements = soup.find_all("div", {"class": "match-info-row"})[2].find("div", {"class": "right"}).text
    kills_elements = kills_elements.replace("\n", "").strip().replace(" :", "").split(" ")
    return kills_elements


def get_clutches_count(soup):
    clutches_count = soup.find_all("div", {"class": "match-info-row"})[3].find("div", {"class": "right"}).text
    clutches_count = clutches_count.replace("\n", "").strip().replace(" :", "").split(" ")
    return clutches_count


def get_round_history(soup, rounds_count):
    who_win_list = []  # * rounds_count
    result_list = []  # * rounds_count
    rows_elements = soup.find_all("div", {"class": "round-history-team-row"})
    row1, row2 = [], []
    for row_index in range(len(rows_elements) // 2):
        row1_tmp = [round.get("src").replace("/img/static/scoreboard/", "").replace(".svg", "") for round in
                rows_elements[row_index * 2].find_all("img", {"class": "round-history-outcome"})]
        row2_tmp = [round.get("src").replace("/img/static/scoreboard/", "").replace(".svg", "") for round in
                rows_elements[row_index * 2 + 1].find_all("img", {"class": "round-history-outcome"})]
        row1 += row1_tmp
        row2 += row2_tmp

    for round_num in range(rounds_count):
        if row1[round_num] == row2[round_num]:
            break
        if row1[round_num] == "emptyHistory":
            result = get_round_type(row2[round_num])
            who_win = 1
        else:
            result = get_round_type(row1[round_num])
            who_win = 0
        who_win_list.append(who_win)
        result_list.append(result)

    return who_win_list, result_list


def get_players_stats(soup):
    all_players_stats = [[], []]
    teams_elements = soup.find_all("table", {"class": "stats-table totalstats"})
    players_elements = [val.find("tbody").find_all("tr") for val in teams_elements]
    for team_num in range(len(players_elements)):
        for player_element in (players_elements[team_num]):
            kills = player_element.find("td", {"class": "st-kills"}).text.replace("\n", "").strip()
            assist = player_element.find("td", {"class": "st-assists"}).text.replace("\n", "").strip()
            deaths = player_element.find("td", {"class": "st-deaths"}).text.replace("\n", "").strip()
            kast = player_element.find("td", {"class": "st-kdratio"}).text.replace("\n", "").strip()
            kd_diff = player_element.find("td", {"class": "st-kddiff"}).text.replace("\n", "").strip()
            adr = player_element.find("td", {"class": "st-adr"}).text.replace("\n", "").strip().replace("-", "0")
            FK = player_element.find("td", {"class": "st-fkdiff"}).text.replace("\n", "").strip()
            rating = player_element.find("td", {"class": "st-rating"}).text.replace("\n", "").strip()

            kills = kills.replace(" ", "")
            kills = kills[:kills.find("(")]
            assist = assist.replace(" ", "")
            assist = assist[:assist.find("(")]
            kast = kast.replace("%", "")
            kd_diff = kd_diff.replace("+", "")
            FK = FK.replace("+", "")

            all_players_stats[team_num].append(
                [int(kills), int(assist), int(deaths), float(kast), int(kd_diff), float(adr), int(FK), float(rating)])
            # print([int(kills), int(assist), int(deaths), float(kast), int(kd_diff), float(adr), int(FK), float(rating)])
    return all_players_stats


def get_round_type(line):
    if line == "ct_win":
        return 1
    if line == "bomb_defused":
        return 2
    if line == "stopwatch":
        return 3
    if line == "t_win":
        return 4
    if line == "bomb_exploded":
        return 5
