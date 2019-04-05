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

# 依語言瀏覽
def surfLanguage(db, keyword):
    result = []

    for song in db:
        if song["language"] == keyword:
            result.append(song)
    
    if len(result) > 0:
        return result
    else:
        return False

# 瀏覽核心
def SurfCore(db, scope, keyword):
    if scope == "language":
        result = surfLanguage(db, keyword)
        return result
    else:
        return False


# 搜尋核心
def SearchCore(db, scope, keyword):
    keywords = keywordFilter(keyword)
    if scope == "title" and keywords:
        result = titleSearch(db, keywords)
        return result
    else:
        return False
