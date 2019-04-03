import re

def keywordFilter(keyword):
    keyword = keyword.replace("or", " ")
    keyword = keyword.replace(u"\u3000", " ")
    keyword = keyword.replace("+", " ")

    keywords = keyword.split(" ")
    
    return keywords

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


def SearchCore(db, method, keyword):
    keywords = keywordFilter(keyword)

    if method == "title":
        result = titleSearch(db, keywords)

    return result
