import json, sys

uid_head = sys.argv[1]

def decode_lang(lang_code):
    language = {"1": "Chinese",
                "2": "Taiwanese",
                "3": "English",
                "4": "Other"}
    return language[lang_code]

def openDataToJSON():
    if len(sys.argv) == 4:
        try:
            songsdata = open(sys.argv[2], "r")
            return json.load(songsdata)
        except Exception as e:
            print(str(e))
            exit()
            return []
    else:
        print("Usage: datamanager.py [language_code] [inputfile.json] [outputfile.json]")
        exit()
        return []

def id_manager(data):
    id_ = [[], [], []]
    id_temp = []
    id_temp_i = ""
    num_c = ""
    num_i = ""
    for song in data:
        s = ""
        for c in song["id_num"]:
            if c != ' ':
                s = s + c
        ss = s.split('-')
        id_temp.append(ss)
    for i in range(len(id_temp)):
        num_c = id_temp[i][0]
        num_i = id_temp[i][1]
        if int(id_temp[i][0]) < 10:
            id_temp[i][0] = '0' + id_temp[i][0]
        id_temp[i][0] = str(uid_head) + '0' + id_temp[i][0]
        id_temp[i][1] = '0' + id_temp[i][1]
        id_[0].append(int(id_temp[i][0] + id_temp[i][1]))
        id_[1].append(int(num_c))
        id_[2].append(int(num_i))
    return id_

def title_manager(data):
    title_ = []
    tonality_ = []
    title_temp = []
    title_temp_a = []
    for song in data:
        title_temp.append(song["song_title"].split(' '))

    for i in range(len(title_temp)):
        temp = []
        if len(title_temp[i]) == 1:
            title_temp[i].append('xyz')
        for j in range(len(title_temp[i])):
            if title_temp[i][j] != '':
                temp.append(title_temp[i][j])
        title_temp_a.append(temp)

    for t in title_temp_a:
        if len(t) == 1:
            tonality_.append('xyz')
            title_.append(t[0])
        else:
            tonality_.append(t[-1])
            if len(t) == 2:
                title_.append(t[0])
            else:
                ti_temp = ""
                for ti in range(len(t)):
                    if ti != len(t) - 1:
                        if ti != len(t) -2:
                            ti_temp = ti_temp + t[ti] + " "
                        else:
                            ti_temp = ti_temp + t[ti]
                title_.append(ti_temp)
    
    tonality_ = [to.replace('xyz', '') for to in tonality_]
                
    return title_, tonality_

def album_manager(data):
    album_ = []

    for song in data:
        album_.append(song["from_where"])

    return album_

def data_manager(data, id_, title, tonality, album, language):
    data_ = []
    data_length = len(data)
    
    for i in range(data_length):
        data_.append({
            "uid": str(id_[0][i]), # 唯一識別編號
            "num_c": str(id_[1][i]), # 檔號：集
            "num_i": str(id_[2][i]), # 檔號：首
            "title": title[i], # 標題、曲名
            "year": "", # 年份
            "singer": "", # 演唱者
            "lyricist": "", # 作詞者
            "composer": "", # 作曲者
            "translater": "", # 翻譯者
            "lyrics": [], # 歌詞
            "tonality": tonality[i], # 調性
            "tempo": "", # 速度
            "time_signature": "", # 拍號
            "album": album[i], # 專輯、詩集
            "publisher": "", # 出版者、發行者
            "ppt_url": "", # 投影片連結
            "sheet_music_url": "", # 歌譜連結
            "language": language # 語言
        })

    return data_

def data_export(data, file):
    out_file = open(file, "w")
    out_file.write(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    data = openDataToJSON()

    output_file = sys.argv[3]

    id_managed = id_manager(data)
    title_managed, tonality_managed = title_manager(data)
    album_managed = album_manager(data)
    # for title in title_managed:
    #     print(title)
    # for to in tonality_managed:
    #     print(to)
    # for title in title_managed:
    #     print(title)
    # for album in album_managed:
    #     if album != '':
    #         print(album)

    # if len(title_managed) == len(tonality_managed) == len(data) == len(album_managed):
    #     print(True)

    data_managed = data_manager(data, id_managed, title_managed, tonality_managed, album_managed, decode_lang(uid_head))

    data_export(data_managed, output_file)
