# services/searchServer.py

import re
from caten_worship.models import songsDB


# 關鍵字過濾器
def keyword_filter(keyword):
    replaceList = [u"\u3000", "+"]
    for string in replaceList:
        keyword = keyword.replace(string, " ")

    keywords = keyword.split(" ")

    if len(keywords) > 0:
        for i in range(len(keywords)):
            j = 0
            if keywords[j] == "":
                keywords.pop(j)
            else:
                j += 1
        return keywords
    else:
        return False


# 以標題搜尋
def search_title(keywords):
    result = []

    for song in songsDB:
        matchs = []
        for word in keywords:
            matchs.append(re.search(word, song["title"]))
        if None not in matchs:
            result.append(song)

    if len(result) > 0:
        return result
    else:
        return False

# 依語言瀏覽
def surf_language(keyword):
    result = []
    
    language = ""
    langCode = keyword[0]
    collection = keyword.replace(keyword[0], "")
    if langCode == "c":
        language = "Chinese"
    elif langCode == "t":
        language = "Taiwanese"
    else:
        return False

    for song in songsDB:
        if song["language"] == language:
            if song["num_c"] == collection:
                result.append(song)
    
    if len(result) > 0:
        return result
    else:
        return False

# 瀏覽核心
def surf_songs(scope, keyword):
    if scope == "language":
        result = surf_language(keyword)
        return result
    else:
        return False


# 搜尋核心
def search_songs(scope, keyword):
    keywords = keyword_filter(keyword)
    if scope == "title" and keywords:
        result = search_title(keywords)
        return result
    else:
        return False
