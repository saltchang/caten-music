# [Caten Music](https://music.caten-church.org)

A music web application for **[Caten Church](https://caten-church.org)**.

- View and search the songs you need.
- Signing up to create a song list and share it to your partner.
- Become an admin and create a new song, or edit an old one.

- See **[Changelog](https://github.com/saltchang/caten-music/blob/master/CHANGELOG.md)**
- Also see **[Church Music API](https://github.com/saltchang/church-music-api)**

## Stack

- [Python](https://www.python.org)
- [Flask](https://flask.palletsprojects.com)
- [PostgreSQL](https://www.postgresql.org)
- [Docker](https://www.docker.com)
- [DropBox API](https://www.dropbox.com/developers/documentation/http/overview)

## Released

### [0.6.0] - 2020-11-27

- Update church music api url

## Quick Start

### Installation

To launch the app locally and quickly, use the sample env file.  
Run the command to create a local environment file from default:

```bash
cp env.example .env
```

See [Environment Variables](#environment-variables) for more information.

### Build & Run

Make sure you have [Docker](https://www.docker.com) installed and then continue.

1. Build the app with docker-compose:

    ```bash
    docker-compose build
    ```

2. Launch the app:

    ```bash
    docker-compose up -d
    ```

    Visit [http://localhost:5000](http://localhost:5000) then you will see the website.

3. See log of the service

    - Use the terminal:

    ```bash
    docker-compose logs -f
    ```

    - Or use your docker GUI

### Environment Variables

The format of the `.env` file must be like the following content:

```env

DROPBOX_ACCESS_TOKEN=<Dropbox_API_token>
DATABASE_URL=<DATABASE_URL>
APP_SETTING=<Mode:[Production, Development, Testing]>
TEST_SETTING=Testing
=<Mail_Account_Username>
HASH_SALT=<Hash_Salt>
SECRET_KEY=<Secret_Key>

```

## Backup Database

To backup the database, use the `backup_db` script, please try:

```bash
./backup_db.sh --help
```

The default backup directory is `./backups`.
