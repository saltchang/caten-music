import re


# 關鍵字過濾器
def keywordFilter(keyword):
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
def titleSearch(db, keywords):
    result = []

    for song in db:
        matchs = []
        for word in keywords:
            matchs.append(re.search(word, song["title"]))
        if None not in matchs:
            result.append(song)

    if len(result) > 0:
        return result
    else:
        return False


# 引擎核心
def SearchCore(db, method, keyword):
    keywords = keywordFilter(keyword)

    if method == "title" and keywords:
        result = titleSearch(db, keywords)
        return result
    else:
        return False
