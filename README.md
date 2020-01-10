# Caten Music

A Flask music app for church.

本專案為歌曲資料庫網站，提供給 **[Caten-Church](https://caten-church.com)** 使用。

- **[Caten Music](https://caten-music.herokuapp.com) - 0.4.0 發佈於 2020-01-10**

- **[Changelog 查看日誌](https://github.com/saltchang/caten-music/blob/master/CHANGELOG.md)**

## Tech Stack

- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org/)
- [Docker](https://www.docker.com/)
- [Heroku](https://www.heroku.com/home)
- [PostgreSQL](https://www.postgresql.org/)
- [DropBox API](https://www.dropbox.com/developers/documentation/http/overview)
- [Church Music API (Go & MongoDB)](https://github.com/saltchang/church-music-api)

## Released

### [0.4.0] - 2020-01-10

- 修改 Docker 設定, 現在可以更快速的在新環境建構專案
- 更新 套件安全性

## Usage

### Clone and Set Environment

Clone the repository and enter it:

```bash

git clone https://github.com/saltchang/caten-music.git

cd caten-music

```

Create the .env file:

```bash

touch .env
```

Add the following content into `.env`:

```env

DROPBOX_ACCESS_TOKEN=<Dropbox_API_token>
DATABASE_URL=<DATABASE_URL>
DATABASE_URL_FOR_TESTING = <DATABASE_URL_FOR_TESTING>
APP_SETTING=<Mode:[Production, Development, Testing]>
TEST_SETTING=Testing
MAIL_USERNAME=<Mail_Account_Username>
MAIL_PASSWORD=<Mail_Account_Password>
HASH_SALT=<Hash_Salt>
SECRET_KEY=<Secret_Key>
FLASK_APP=run.py

```

To quick user the sample env file,  
run the command, to rename it:

```bash

mv env.test .env
```

You must change the `<variable>` by your case.

### Build & Run

Build Docker-Compose

```bash

docker-compose build
```

Run Docker-Compose

```bash

docker-compose up -d
```

Visit [http://localhost:5000](http://localhost:5000) then you will see it.

### See log of the service

```bash

docker-compose logs -f
```
