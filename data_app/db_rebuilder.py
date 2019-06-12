import json, sys

def loadJsonFile():
    if len(sys.argv) == 4:
        try:
            new_data = open(sys.argv[1], "r")
            original_data = open(sys.argv[2], "r")
            return [json.load(original_data), json.load(new_data)]
        except Exception as e:
            print(str(e))
            exit(2)
    else:
        print("Usage: db_rebuilder.py [newdata.json] [origin.json] [output.json]")
        exit(1)

def updateData(originalData, newData):
    
    for originalSong in originalData:

        for newSong in newData:

            if not len(newSong["sid"]) == 7:
                print("(注意!) SID 格式錯誤: ", song["sid"])
            
            if not "sid" in newSong:
                print("Error: New data has no 'SID' information.")
                exit(3)

            if originalSong["sid"] == newSong["sid"]:
                if "lyrics" in newSong:
                    originalSong["lyrics"] = newSong["lyrics"]

    return originalData

            # Old Stuff...
            # newSongs.append(
            #     {
            #     "sid": song["sid"], # 唯一識別編號
            #     "num_c": song["num_c"], # 檔號：集
            #     "num_i": song["num_i"], # 檔號：首
            #     "title": song["title"], # 標題、曲名
            #     "year": song["year"], # 年份
            #     "lyricist": song["lyricist"], # 作詞者
            #     "composer": song["composer"], # 作曲者
            #     "translator": song["translator"], # 翻譯者
            #     "lyrics": song["lyrics"], # 歌詞
            #     "tonality": song["tonality"], # 調性
            #     "tempo": song["tempo"], # 速度
            #     "time_signature": song["time_signature"], # 拍號
            #     "album": song["album"], # 專輯、詩集
            #     "publisher": song["publisher"], # 出版者、發行者
            #     "language": song["language"] # 語言
            #     }
            # )


def exportData(outputData, outputFile):
    out_file = open(outputFile, "w")
    out_file.write(json.dumps(outputData, ensure_ascii=False))

# Run App
if __name__ == "__main__":

    data = loadJsonFile()

    outputData = updateData(data[0], data[1])

    outputFile = sys.argv[3]

    exportData(outputData, outputFile)
