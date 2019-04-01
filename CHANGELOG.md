# Changelog

這是"茄典教會詩歌資料系統"的開發日誌

- By David KuangYen Chang

## [Unrelease]

## [0.0.5] - 2019-03-31

### Todo

- 測試：以彈出視窗預覽歌譜
- 資料庫結構更新：歌詞、作詞、作曲
- 新增：供使用者回報歌曲資料錯誤功能
- 新增：搜尋引擎

### Added

- 新增 static/js/main.js
- 新增 投影片及歌譜下載的 try & except
- 新增 static/image/log/favicon.ico

### Changed

- 重建列表結構及樣式（ table -> list card ）
- 調整 RWD 效果以手機使用者角度為主
- 調整介面顏色

### Removed

- 移除 all_songs.html 中的歌曲 table 架構

## [0.0.4] - 2019-03-30

### Todo

- 以彈出視窗預覽歌譜，並提供下載按鈕（測試中）
- 預計移除 table 結構，改採 list 結構..

### Added

- 建立 Dropbox API
- 新增 兩個功能：顯示歌譜、下載PPT
- 建立 img.html 暫作測試用途
- 新增 Navbar
- 建立 static 資料：網站LOGO

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
- 整理檔案結構，重新部署

## [0.0.2] - 2019-03-27

### Added

- 建立 .markdownlint.json 並且設定 MD024 為 false
- 新增列出所有歌曲清單功能
- 獨立 importDB 功能至 importDB.py
- 獨立 app.config 至 config.py

### Changed

- 修改 datamanager.py 功能
- 修改資料庫檔案
- 修改介面：所有詩歌列表

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

- 這是一個基於 Python Flask, Heroku 的網路應用，提供給茄典教會敬拜及音樂服事同工使用

## Cheat sheet

- Added
- Changed
- Fixed
- Removed