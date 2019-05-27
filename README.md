# Caten Worship

本專案為歌曲資料庫網站,
網址為 [https://caten-worship.herokuapp.com](https://caten-worship.herokuapp.com)

提供給 [茄典教會](https://caten-church.com) 使用

詳細開發日誌請查看 [CHANGELOG.md](https://github.com/saltchang/caten-worship/blob/master/CHANGELOG.md)

## Released

### [0.1.7] - 2019-05-20

- 連接 歌曲資料庫 [API](https://github.com/saltchang/church-music-api)

## Stack

- [Flask](http://flask.pocoo.org/)
- [Heroku](https://www.heroku.com/home)
- [PostgreSQL](https://www.postgresql.org/)
- [DropBox API](https://www.dropbox.com/developers/documentation/http/overview)
- [Church Music API](https://github.com/saltchang/church-music-api)

## Usage

### Clone and Set Environment

Clone the file into your local repository:

```shell

$ git clone https://github.com/saltchang/caten-worship.git

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

DROPBOX_ACCESS_TOKEN=<Your Dropbox API token>
DATABASE_URL=<Your PostgreSQL URL>
DATABASE_URL_FOR_TESTING=<Your PostgreSQL URL for testing>
APP_SETTING="config.Config.Development"
TEST_SETTING="config.Config.Testing"
MAIL_USERNAME=<Your mail account username>
MAIL_PASSWORD=<Your mail account password>
HASH_SALT=<Set your own salt for hashing>
SECRET_KEY=<Your secret key>
FLASK_APP=run.py
FLASK_ENV=development

```

and change the `<variable>`

### PSQL Migration

Create the needed database (in pipenv):

```shell

$ pipenv run flask db upgrade

```

## Run

Run in flask way:

```shell

$ pipenv run flask run

```

Run in Heroku way:

(If you have [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed)

```shell

$ pipenv run heroku local web

```
