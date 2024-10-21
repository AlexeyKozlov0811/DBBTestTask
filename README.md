DBBTestTask
====

### Local Install

Get code from repository:
https://github.com/AlexeyKozlov0811/DBBTestTask

We use `pipenv`
https://pipenv.pypa.io/en/latest/ (to install it on Ubuntu/Debian:
`sudo apt install pipenv`)

Install Python packages

```bash
pipenv install -d
```

### Copy the .env file

   ```bash
   cp .env.example .env
   ```

### DB set up

SQLite DB can be retrieved from github `database.db` if it's not present, empty db will be created upon starting server

### Run Local Server

```bash
python -m uvicorn main:app
```

### Use app

1. Go to the docs page http://127.0.0.1:8000/docs#/
2. Register a user using endpoint `/api/users/register/`
3. Log in via **Authorize** button on top of the page using your username and password
4. Have fun
