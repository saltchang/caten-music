# Caten Worship

A Flask music app for church.

本專案為歌曲資料庫網站，提供給 **[Caten-Church](https://caten-church.com)** 使用。

- **[Caten Worship](https://caten-worship.herokuapp.com) - 0.2.0 已發佈**

- **[Changelog 查看日誌](https://github.com/saltchang/caten-worship/blob/master/CHANGELOG.md)**

## Tech Stack

- [Python](https://www.python.org/)
- [Pipenv](https://github.com/pypa/pipenv)
- [Flask](http://flask.pocoo.org/)
- [Heroku](https://www.heroku.com/home)
- [PostgreSQL](https://www.postgresql.org/)
- [DropBox API](https://www.dropbox.com/developers/documentation/http/overview)
- [Church Music API (Go & MongoDB)](https://github.com/saltchang/church-music-api)

## Released

### [ v0.2.0 ] - 2019-06-15

- 新增 歌單功能（建立、編輯、刪除、分享、加入歌曲、移除歌曲）
- 新增 重設密碼功能
- 調整 使用者介面
- 改善 彈出式通知功能
- 修正 認證問題

## Usage

### Clone and Set Environment

Clone the repository and enter it:

```shell

$ git clone https://github.com/saltchang/caten-worship.git

$ cd caten-worship

```

Use [Pipenv](https://github.com/pypa/pipenv) for managing dependencies:

```shell

$ pipenv install

```

Create the .env file:

```shell

$ touch .env

```

Add the following content into .env:

```text

DROPBOX_ACCESS_TOKEN = <Your Dropbox API token>
DATABASE_URL = <Your PostgreSQL URL>
DATABASE_URL_FOR_TESTING = <Your PostgreSQL URL for testing>
APP_SETTING = "config.Config.Development"
TEST_SETTING = "config.Config.Testing"
MAIL_USERNAME = <Your mail account username>
MAIL_PASSWORD = <Your mail account password>
HASH_SALT = <Set your own salt for hashing>
SECRET_KEY = <Your secret key>
FLASK_APP = run.py
FLASK_ENV = development

```

You must change the `<variable>` by your case.

### Database Migration

Create (migrate) the needed database (in pipenv):

```shell

$ pipenv run flask db upgrade

```

### Test

Before you run the app, please test it first:

```shell

$ pipenv run pytest

```

### Run

Run in flask way:

```shell

$ pipenv run flask run

```

Run in Heroku way:

(If you have [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed)

```shell

$ pipenv run heroku local web

```
