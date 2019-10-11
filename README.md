# Caten Music

A Flask music app for church.

本專案為歌曲資料庫網站，提供給 **[Caten-Church](https://caten-church.com)** 使用。

- **[Caten Music](https://caten-music.herokuapp.com) - 0.3.0 發佈於 2019-10-12**

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

### [ v0.3.0 ] - 2019-10-12

- Dockerized

## Usage

### Clone and Set Environment

Clone the repository and enter it:

```shell

$ git clone https://github.com/saltchang/caten-music.git

$ cd caten-music

```

Create the .env file:

```shell

$ touch .env

```

Add the following content into .env:

```text

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

You must change the `<variable>` by your case.

### Build & Run

Build the Docker image

```shell

$ docker build -t caten_music . --no-cache

```

Run from the Docker image

```shell

$ docker run --env-file .env caten_music

```

### Connect from the local machaine

```shell

# Run this command, and find your <CONTAINER ID>

$ docker ps

# The PORTS column should be "5000/tcp"

```

```shell

# Then, run the following command

$ docker inspect <CONTAINER ID>

# You will find the docker machine id in "IPAddress"

```

open your browser and connect to `<IPAddress>:5000`

you will see the website.
