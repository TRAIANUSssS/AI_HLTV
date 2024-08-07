def get_player_name(soup):
    name_element = soup.find("h1").text.replace("\n", "").strip()
    return name_element


def get_stats_from_stat_box(soup):
    stats_elements = soup.find_all("div", {"class": "stats-row"})
    # if soup.find("h1").text.replace("\n", "").strip() == "icyvl0ne":
    #     print(stats_elements[0].text.replace("\n", "").strip())
    if stats_elements[0].text.replace("\n", "").replace(" ", "") == "Totalkills0":
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    stats_list = []
    for stat_index, stat_element in enumerate(stats_elements):
        stat_val = stat_element.find_all("span")[1].text.replace("\n", "").strip().replace("%", "")
        stat_val = float(stat_val) if stat_val.count(".") else int(stat_val)
        if stat_index not in [3, 5, 11, 12]:
            stats_list.append(stat_val)
    return stats_list


def get_rating_vs_tops(soup):
    rating_elements = soup.find_all("div", {"class": "rating-value"})
    rating_vals = [val.text.replace("\n", "").strip() for val in rating_elements[:4]]
    rating_vals = [None if val == "-" else val for val in rating_vals]
    return rating_vals


def get_maps_vs_tops(soup):
    maps_elements = soup.find_all("div", {"class": "rating-maps"})
    maps_vals = [val.text.replace("\n", "").strip() for val in maps_elements[:4]]
    maps_vals = [int(val.replace("(", "")[:val.find("") + 1]) for val in maps_vals]
    return maps_vals


def get_kast_and_impact(soup):
    stats_elements = soup.find_all("div", {"class": "summaryStatBreakdownDataValue"})
    kast = stats_elements[2].text.replace("\n", "").strip().replace("%", "")
    impact = stats_elements[3].text.replace("\n", "").strip()
    return kast, impact


def get_age(soup, date):
    age = soup.find("div", {"class": "summaryPlayerAge"}).text.replace("\n", "").strip()
    age = age[:age.find(" ")]
    age = int(age) - date // (24 * 3600 * 365) if age != "" else 21
    return age


def get_data_from_individual_page(soup):
    stats_elements = soup.find_all("div", {"class": "stats-row"})
    if stats_elements[0].text.replace("\n", "").strip() == "0":
        return [[0, 0, 0, 0, 0], 0, 0, 0, 0, 0, 0]
    round_stats = stats_elements[12:18]
    round_stats = [round_stat.text.replace("\n", "").strip()[2:].replace("kill rounds", "").strip() for
                   round_stat in round_stats]

    open_stats = stats_elements[6:10]
    new_open_stats = []
    for open_stat in open_stats:
        open_stat = open_stat.text.replace("\n", "").strip()
        open_stat = open_stat[::-1]
        open_stat = open_stat[:open_stat.find(" ")]
        open_stat = open_stat[::-1]
        new_open_stats.append(open_stat)

    weapon_stats = stats_elements[18:20]
    weapon_stats = [weapon_stat.text.replace("\n", "").strip() for
                    weapon_stat in weapon_stats]
    weapon_stats = [''.join(filter(str.isdigit, weapon_stat)) for weapon_stat in weapon_stats]

    return_list = [round_stats]
    return_list += new_open_stats + weapon_stats

    return return_list
