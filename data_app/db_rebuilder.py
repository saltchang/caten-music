import json, sys

def loadJsonFile():
    if len(sys.argv) == 3:
        try:
            songsdata = open(sys.argv[1], "r")
            return json.load(songsdata)
        except Exception as e:
            print(str(e))
            exit(1)
    else:
        print("Usage: db_rebuilder.py [inputfile.json] [outputfile.json]")
        exit(1)

def rebuildData(originSongs):

    newSongs = []
    
    for song in originSongs:

        if not len(song["sid"]) == 7:
            print(song["sid"])

        newSongs.append(
            {
            "sid": song["sid"], # 唯一識別編號
            "num_c": song["num_c"], # 檔號：集
            "num_i": song["num_i"], # 檔號：首
            "title": song["title"], # 標題、曲名
            "year": song["year"], # 年份
            "lyricist": song["lyricist"], # 作詞者
            "composer": song["composer"], # 作曲者
            "translator": song["translator"], # 翻譯者
            "lyrics": song["lyrics"], # 歌詞
            "tonality": song["tonality"], # 調性
            "tempo": song["tempo"], # 速度
            "time_signature": song["time_signature"], # 拍號
            "album": song["album"], # 專輯、詩集
            "publisher": song["publisher"], # 出版者、發行者
            "language": song["language"] # 語言
            }
        )

    return newSongs

def data_export(data, output_file_name):
    out_file = open(output_file_name, "w")
    out_file.write(json.dumps(data, ensure_ascii=False))

# Run App
if __name__ == "__main__":

    originSongsData = loadJsonFile()

    newSongs = rebuildData(originSongsData)

    output_file_name = sys.argv[2]

    data_export(newSongs, output_file_name)
