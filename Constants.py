import os

MAIN_PATH = os.getcwd() + "/"

MONTHS = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december",
}

MONTHS_INVERSE = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

headers_for_ranking_stats = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.hltv.org/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

headers_for_result_page = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'https://www.hltv.org/results',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

headers_for_match_page = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.hltv.org/results',
    'Connection': 'keep-alive',
    # 'Cookie': 'MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; CookieConsent={stamp:%27dX/FfGexLu3TDHMv2CIa6yixcni1A8lNJQccthpxSF+Rkei6dvhBXw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1718977904650%2Cregion:%27ru%27}; _ga_525WEYQTV9=GS1.1.1719059186.4.0.1719059186.0.0.0; _ga=GA1.1.251624430.1718977905; cf_clearance=XnQJz4c.yUeiAtq3quN5d9mmoKFebP338ub2CeLH3ws-1718980008-1.0.1.1-11JlfV7qrDll24WXiXYV35QUh8bwTYSYEadbUXLmAI7tOd0a0RoEEoKFy5OIkrGC7XmoAZAF_qf4VSY1CcGbxQ; __cf_bm=fzLbukkoUMLPCtCRTxnV7ebyzoCmU9BZSMOOB_ytEms-1719059189-1.0.1.1-t5o7cRGhX9FjS.1Wz.xyhyaOnFd7ng9l13q0WzVM0vFfD7oiq4iQ6Q7659wUktAKaKWVrR5f0gxjuIlfZxvoHA; dicbo_id=%7B%22dicbo_fetch%22%3A1719059189188%7D',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}
