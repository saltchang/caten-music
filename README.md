# Caten Music

A Flask music app for church.

本專案為歌曲資料庫網站，提供給 **[Caten-Church](https://caten-church.org)** 使用。

- **[Caten Music](https://caten-music.herokuapp.com) - 0.5.0 發佈於 2020-02-22**

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

### [0.5.0] - 2020-02-22

- 新增 新增歌曲功能

## Usage

### Clone and Set Environment

Clone the repository and enter it:

```bash

git clone https://github.com/saltchang/caten-music.git

cd caten-music
```

To quick use the sample env file,  
run the command to rename it for using:

```bash

cp env.test .env
```

The format of env file must be like following content:

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

You can change the `<variable>` as your wish.

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
