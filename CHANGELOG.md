# Changelog

這是"茄典教會詩歌資料系統"的開發日誌

- By David KuangYen Chang

## [Unrelease]

### Todo

- 功能: 以彈出視窗預覽歌譜
- 功能: 新增歌曲
- 功能: 依多重條件選歌
- 功能: 登入、註冊

## [0.0.10] - 2019-04-09

### Added

- 更新 ppt 資料
- 新增 依語言、集數瀏覽詩歌

### Changed

- 更改 Dropbox API Token
- 調整 介面樣式
- 修改 依語言瀏覽程式

## [0.0.9] - 2019-04-05

### Added

- 新增 字型: "EB Garamond", "Noto Sans TC", "Noto Serif TC" from Google Fonts
- 新增 CSS Reset /static/css/reset.css
- 新增 package: psycopg2
- 新增 app.route("/surfer") 瀏覽功能
- 新增 surfer.html 介面, static/css/surfer.css
- 新增 surfCore 瀏覽引擎
- 新增 Heroku Postgresql 資料庫, 已完成資料庫連接測試
- 新增 users.html 作資料庫測試用途

### Changed

- 更改 App name: caten-worship.py > catenWorship.py
- 優化 搜尋引擎

### Removed

- 移除 瀏覽所有詩歌

## [0.0.8] - 2019-04-04

### Added

- 新增 Pipfile 和 Pipfile.lock
- 將 CSS 從 html 中獨立出來至 /static/css/*.css
- 新增 menuicon.png
- 新增 YouTube 連結功能

### Removed

- 移除 requirements.txt
- 移除 template: allsongs.html

### Changed

- 將所有 template 之副檔名更改 *.html > *.jinja
- 將運行環境更改為pipenv
- 將 allsongs.html 整合至 result.html 中
- 更改介面配色: 扁平化色調

### Fixed

- 修正搜尋引擎之錯誤情形以及避免空關鍵字觸發所有結果 searchEngine.py

## [0.0.7] - 2019-04-03

### Added

- 建立 搜尋引擎 searchEngine.py
- 新增 app.route("/search")
- 新增 首頁: 搜尋

### Changed

- 調整版面結構
- 將瀏覽所有詩歌連結移至Navbar

## [0.0.6] - 2019-04-03

### Added

- 新增 excel 資料匯入程式
- 新增 Song Crawler 歌曲資訊爬蟲程式 /songs_data/db_app/song_crawler/
- 新增 db_matcher.py: 比對資料庫資料的程式 /songs_data/db_app/db_matcher.py
- 建立 /songs_data/json/library/songDB_got.json 作為歌曲的資料庫之一
- 匯集網路爬蟲資料完成
- 建立 worshipDB.json 為主資料庫 /songs_data/json/DB/worshipDB.json

### Changed

- 修改 .gitignore
- 資料庫結構更新: 增加 "歌詞、作詞、作曲、出版、演唱、速度、拍號、年份"
- 將歌詞從資料庫的歌詞陣列中以迴圈方式讀取出來
- 修改: 改善折疊清單之互動按鈕觸發範圍以及效果
- 更名 datamanager.py > db_creator.py
- 更新資料庫

## [0.0.5] - 2019-03-31

### Added

- 新增 static/js/main.js
- 新增 投影片及歌譜下載的 try & except
- 新增 static/image/log/favicon.ico

### Changed

- 重建列表結構及樣式(table -> list card)
- 調整 RWD 效果以手機使用者角度為主
- 調整介面顏色

### Removed

- 移除 all_songs.html 中的歌曲 table 架構

## [0.0.4] - 2019-03-30

### Added

- 建立 Dropbox API
- 新增 兩個功能: 顯示歌譜、下載PPT
- 建立 img.html 暫作測試用途
- 新增 Navbar
- 建立 static 資料: 網站LOGO

### Changed

- 修改 all_songs.html
- 更新 requirements.txt

### Fixed

- 調整響應式介面

## [0.0.3] - 2019-03-29

### Added

- 建立 secret.txt

### Changed

- 加入 secret.txt 至 .gitignore

### Fixed

- 將 secret key 從 config.py 中移除
- 整理檔案結構, 重新部署

## [0.0.2] - 2019-03-27

### Added

- 建立 .markdownlint.json 並且設定 MD024 為 false
- 新增列出所有歌曲清單功能
- 獨立 importDB 功能至 importDB.py
- 獨立 app.config 至 config.py

### Changed

- 修改 datamanager.py 功能
- 修改資料庫檔案
- 修改介面: 所有詩歌列表

## [0.0.1] - 2019-03-25

### Added

- 建立 caten-worship.py
- 建立 datamanager.py
- 建立暫時資料庫 songs_data
- 建立 CHANGELOG.md
- 建立 .gitignore
- 建立 requirements.txt
- 建立 README.md
- 建立 runtime.txt, Procfile

## Initial Information

- 這是一個基於 Python Flask, Heroku 的網路應用, 提供給茄典教會敬拜及音樂服事同工使用

## Cheat sheet

- Added
- Changed
- Fixed
- Removed