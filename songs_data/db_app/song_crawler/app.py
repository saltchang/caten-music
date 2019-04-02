# -*- coding: UTF-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup

start = 5000
end = start + 500

locat = "./output/"

songs = []
outFileName = "c_" + str(start) + "_" + str(end - 1) + ".json"
outFileURL = locat + outFileName
outFile = open(outFileURL, "w")

processCounter = 1
ran = end - start

print()
for i in range(start, end):
    try:
        result = requests.get(
            "http://www.christianstudy.com/data/hymns/text/c" + str(i) + ".html")
        result.encoding = "big5"

        soup = BeautifulSoup(result.text, "html.parser")
        sel = soup.select("p font")
        pick = soup.select("p")

        song = {"id_": "",
                "title": "",
                "lyrics": [],
                "album": "",
                "lyricist": "",
                "composer": "",
                "translator": ""
                }
        ss = []
        for s in sel:
            ss.append(s.text.split("\n\r\n"))

        song["id_"] = str(i)
        song["title"] = ss[0][0].replace("【", "").replace("】", "")

        for part in ss[1]:
            part = part.splitlines()
            p = ["p"]
            for line in part:
                if line != "":
                    line = line.replace(" ", "").replace("　", "")
                    p.append(line)
            song["lyrics"].append(p)

        head_ = str(pick[0]).splitlines()[1].replace(
            "</p>", "").replace("\x02", "").replace(" ", "")
        # print("\"" + head_ + "\"")
        head = re.split(u"\u3000" + "|<br/>" + "|；" + "|／", head_)

        for h in head:

            album_l = ["詩集："]
            l_c = ["曲、詞：", "詞、曲：", "詞曲：", "曲詞：", "曲/詞：", "詞/曲："]
            trans = ["中譯詞：", "譯詞：", "中譯：", "譯者：", "譯："]
            ly = ["填詞：", "作詞：", "詞："]
            co = ["作曲：", "曲："]

            if any(re.findall('|'.join(album_l), h)):
                for rep in album_l:
                    h = h.replace(rep, "")
                song["album"] = h

            elif any(re.findall('|'.join(l_c), h)):
                for rep in l_c:
                    h = h.replace(rep, "")
                song["lyricist"] = h
                song["composer"] = h

            elif any(re.findall('|'.join(trans), h)):
                for rep in trans:
                    h = h.replace(rep, "")
                song["translator"] = h

            elif any(re.findall('|'.join(ly), h)):
                for rep in ly:
                    h = h.replace(rep, "")
                song["lyricist"] = h

            elif any(re.findall('|'.join(co), h)):
                for rep in co:
                    if h.find("編曲") == -1:
                        h = h.replace(rep, "")
                song["composer"] = h

        header = []

        # print(pick[0].split("<br>").text.splitlines()[1])
        songs.append(song)
        f = (processCounter/ran) * 100
        print("[ %.1f" % (f) + "% ] " + "編號：" + str(i) + " - 歌曲資料擷取成功")
        processCounter += 1
    except Exception as error:
        f = (processCounter/ran) * 100
        print("[ %.1f" % (f) + "% ] " + "編號：" +
              str(i) + " - 歌曲資料擷取失敗：\n" + str(error))
        processCounter += 1
    print()

    

outFile.write(json.dumps(songs, ensure_ascii=False))
