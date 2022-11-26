# Changelog

## Released

### [0.5.2] - 2020-11-27

- Update to support new version packages

## History

### [0.5.1] - 2020-02-02

- Fix default environment file for building the app in development  
  (miss env variable: DATABASE_URL_FOR_DEVELOPMENT)

### [0.5.0] - 2020-02-22

#### Added

- New feature: create new songs

### [0.4.0] - 2020-01-10

#### Added

- 新增 測試用 env 檔案, 並更新 README.md
- 新增 postgres 至 docker-compose
- 新增 'development' 環境標籤於首頁

#### Changed

- 修改 .gitignore
- 更新 套件安全性

### [0.3.0] - 2019-10-12

- Dockerized

### [0.2.8] - 2019-08-14

#### Added

- 新增欄位 原文歌名、原文出版、經文

#### Fixed

- 修正 無法保留歌詞空白的問題，現在只會自動消去頭尾的多餘空白

#### Changed

- 調整介面

### [0.2.7] - 2019-07-24

#### Added

- 新增 總管權限 - 編輯使用者資料

### [0.2.6] - 2019-07-21

#### Added

- 新增 管理員權限 - 編輯歌曲資料

### [0.2.5] - 2019-07-21

#### Added

- 新增 依調性分類瀏覽

### [0.2.4] - 2019-07-18

#### Added

- 新增 歌譜下載功能

#### Fixed

- 歌曲資料整理
- 前端介面調整

### [0.2.3] - 2019-07-13

#### Added

- 新增 歌曲回報功能
- 新增 依歌詞搜尋

### [0.2.2] - 2019-06-17

#### Changed

- 更名 Caten Worship -> Caten Music
- 更換 Logo

#### Added

- 新增 首頁引導窗
- 新增 隨機推薦歌曲

#### Fixed

- 調整 前端介面

### [0.2.1] - 2019-06-16

#### Added

- 新增 登入紀錄
- 新增 登入、登出後會重新導向回到前一頁面

#### Fixed

- 調整 前端介面
- 調整 註冊提示

### [0.2.0] - 2019-06-15

#### Added

- 完成 歌單頁面
- 完成 新增歌單
- 完成 加入歌曲至歌單
- 完成 編輯歌單
- 完成 刪除歌單
- 完成 Line 分享歌單
- 完成 重設密碼

#### Fixed

- 調整 前端介面

### [0.1.8] - 2019-05-29

*Unrelease*

#### Added

- 新增 個人歌單資料庫欄位
- 新增 我的歌單 頁面
- 新增 歌單模板

#### Changed

- 調整 歌曲資料介面
- 將各框架及函式庫由 CDN 轉移至 本地檔案
- 重寫 README.md
- 忽略 MD036(.markdownlint.json)

#### Fixed

- 修正 database.py
- 修正 flask-migrate
- 整理專案檔案
- 修正 一些 URL 連結錯誤
- 修正 一些檔案名稱

#### Removed

- 移除不必要的檔案

### [0.1.7] - 2019-05-20

#### Added

- 連結 歌曲資料庫API - [(church-music-api)](https://github.com/saltchang/church-music-api)

### [0.1.6] - 2019-05-01

#### Added

- 新增 資料庫遷徙功能 flask-migrate

#### Fixed

- 修正 已啟動帳號現在不再能再申請寄送帳號啟動信

### [0.1.5] - 2019-04-30

#### Added

- 新增 單元測試: routes.download_ppt
- 新增 單元測試: routes.register
- 新增 單元測試: routes.login
- 新增 單元測試: routes.logout
- 新增 單元測試: routes.surfer

### [0.1.4] - 2019-04-25

#### Remark

- 此版本不會部署至 Heroku

#### Added

- 建立 登入功能
- 建立 登出功能
- 建立 重寄帳號啟動信
- 建立 使用者個人檔案資料庫 models.UserProfile
- 新增 alert 進入 base layout
- 新增 dev-login 分支, 嘗試 github flow
- 新增 單元測試: routes.search
- 新增 database.py CLI tool, 用途為快速刪除或建立資料庫

#### Changed

- 更改 前端結構及樣式
- 更改 Logo 及 favicon.ico
- 調整 後端資料庫

#### Fixed

- 修正 表單按 Enter 正確經過認證後提交

### [0.1.3] - 2019-04-19

#### Added

- 建立 db.py, 將資料庫工廠化

#### Changed

- 修改 註冊密碼可容許符號: "_!@#$%^&*+-/:"
- 新增 Heroku ACM, 更改網址
- 調整 models/users.py 結構
- 調整 系統架構

### [0.1.2] - 2019-04-17

#### Added

- **註冊功能完備**
- 建立 前端註冊表單驗證功能
- 建立 後端註冊表單驗證功能
- 建立 註冊時即時AJAX驗證功能
- 建立 一些訊息templates

#### Changed

- 修改 網站Logo
- 調整 前端介面

### [0.1.1] - 2019-04-14

#### Remark

- 由於尚未完成註冊前表單驗證，故此版本未部署

#### Added

- 新增 /register 註冊功能完成
- 新增 flask-mail 註冊時同步寄送認證信至所註冊之信箱
- 新增 /activate/account/check 註冊認證功能完成

#### Changed

- Format 一些檔案

### [0.1.0] - 2019-04-12

#### Changed

- 重建 Flask App 架構 - 模組化
- 導入 Flask Blueprint
- 重建 資料庫

```txt
caten-worship/
  __init__.py
  helper/
    __init__.py
    importJSON.py
    ...
  models/
    __init__.py
    songs.py
    users.py
    ...
  routes/
    __init__.py
    home.py
    search.py
    ...
  services/
    __init__.py
    searchEngine.py
    ...
  templates/
    base.html
    index.html
    ...
  static/
    css/
    image/
    js/
```

### [0.0.10] - 2019-04-09

#### Added

- 更新 ppt 資料
- 新增 依語言、集數瀏覽詩歌

#### Changed

- 更改 Dropbox API Token
- 調整 介面樣式
- 修改 依語言瀏覽程式

### [0.0.9] - 2019-04-05

#### Added

- 新增 字型: "EB Garamond", "Noto Sans TC", "Noto Serif TC" from Google Fonts
- 新增 CSS Reset /static/css/reset.css
- 新增 package: psycopg2
- 新增 app.route("/surfer") 瀏覽功能
- 新增 surfer.html 介面, static/css/surfer.css
- 新增 surfCore 瀏覽引擎
- 新增 Heroku Postgresql 資料庫, 已完成資料庫連接測試
- 新增 users.html 作資料庫測試用途

#### Changed

- 更改 App name: caten-worship.py > catenWorship.py
- 優化 搜尋引擎

#### Removed

- 移除 瀏覽所有詩歌

### [0.0.8] - 2019-04-04

#### Added

- 新增 Pipfile 和 Pipfile.lock
- 將 CSS 從 html 中獨立出來至 /static/css/*.css
- 新增 menuicon.png
- 新增 YouTube 連結功能

#### Removed

- 移除 requirements.txt
- 移除 template: allsongs.html

#### Changed

- 將所有 template 之副檔名更改 *.html > *.jinja
- 將運行環境更改為pipenv
- 將 allsongs.html 整合至 result.html 中
- 更改介面配色: 扁平化色調

#### Fixed

- 修正搜尋引擎之錯誤情形以及避免空關鍵字觸發所有結果 searchEngine.py

### [0.0.7] - 2019-04-03

#### Added

- 建立 搜尋引擎 searchEngine.py
- 新增 app.route("/search")
- 新增 首頁: 搜尋

#### Changed

- 調整版面結構
- 將瀏覽所有詩歌連結移至Navbar

### [0.0.6] - 2019-04-03

#### Added

- 新增 excel 資料匯入程式
- 新增 Song Crawler 歌曲資訊爬蟲程式 /songs_data/db_app/song_crawler/
- 新增 db_matcher.py: 比對資料庫資料的程式 /songs_data/db_app/db_matcher.py
- 建立 /songs_data/json/library/songDB_got.json 作為歌曲的資料庫之一
- 匯集網路爬蟲資料完成
- 建立 worshipDB.json 為主資料庫 /songs_data/json/DB/worshipDB.json

#### Changed

- 修改 .gitignore
- 資料庫結構更新: 增加 "歌詞、作詞、作曲、出版、演唱、速度、拍號、年份"
- 將歌詞從資料庫的歌詞陣列中以迴圈方式讀取出來
- 修改: 改善折疊清單之互動按鈕觸發範圍以及效果
- 更名 datamanager.py > db_creator.py
- 更新資料庫

### [0.0.5] - 2019-03-31

#### Added

- 新增 static/js/main.js
- 新增 投影片及歌譜下載的 try & except
- 新增 static/image/log/favicon.ico

#### Changed

- 重建列表結構及樣式(table -> list card)
- 調整 RWD 效果以手機使用者角度為主
- 調整介面顏色

#### Removed

- 移除 all_songs.html 中的歌曲 table 架構

### [0.0.4] - 2019-03-30

#### Added

- 建立 Dropbox API
- 新增 兩個功能: 顯示歌譜、下載PPT
- 建立 img.html 暫作測試用途
- 新增 Navbar
- 建立 static 資料: 網站LOGO

#### Changed

- 修改 all_songs.html
- 更新 requirements.txt

#### Fixed

- 調整響應式介面

### [0.0.3] - 2019-03-29

#### Added

- 建立 secret.txt

#### Changed

- 加入 secret.txt 至 .gitignore

#### Fixed

- 將 secret key 從 config.py 中移除
- 整理檔案結構, 重新部署

### [0.0.2] - 2019-03-27

#### Added

- 建立 .markdownlint.json 並且設定 MD024 為 false
- 新增列出所有歌曲清單功能
- 獨立 importDB 功能至 importDB.py
- 獨立 app.config 至 config.py

#### Changed

- 修改 datamanager.py 功能
- 修改資料庫檔案
- 修改介面: 所有詩歌列表

### [0.0.1] - 2019-03-25

#### Added

- 建立 caten-worship.py
- 建立 datamanager.py
- 建立暫時資料庫 songs_data
- 建立 CHANGELOG.md
- 建立 .gitignore
- 建立 requirements.txt
- 建立 README.md
- 建立 runtime.txt, Procfile
