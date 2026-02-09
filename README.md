# crPMT Backend
Back end for the Clinical Research Project Management Tool

## Requirements
- Python (tested with 3.11)
- PostgreSQL (tested with 16.4)

## Installation
PostgreSQL:
- Create a `crpmt` DB (and user if you want a dedicated user, in that case don't forget to remove the command with the password in ~/.psql_history!)

Python:
- Create a venv and install the packages from the requirements file
- Create a `configs` folder (in the project root)
    - Create a `configs/app_config.py` file with SECRET_APP_KEY, ALLOWED_APP_HOSTS, USERS_APP_NAME, and CORE_APP_NAME values
    - Create a `configs/db_config.py` file with PG_*_CRPMT_DB db connection values, CRPMT_DB_KEY_NAME (default), USERS_DB_KEY_NAME, and CORE_DB_KEY_NAME values
    - Create a `configs/identity_config.py` file with all OIDC settings (check `crpmt/settings.py`)
- Run `python manage.py migrate` to set up the crpmt DB
- Run `python manage.py loaddata [fixture_name]` where `fixture_name` is the name of a file in `context/fixtures`. Run this for all files in the folder to pre-populate the DB for relevant context models
- TODO: loading CTUs and other links to Microsoft lists

Running crPMT BE as a service (example):
- In `/etc/systemd/system`:
    - Create a `crpmt.socket` file with `ListenStream=/run/crpmt.sock`
    - Create a `crpmt.service` file with `ExecStart=[path/to/gunicorn/in/venv] --workers 7 --bind unix:/run/crpmt.sock crpmt.wsgi`
    - Run the service with systemctl

Running locally:
`python manage.py runserver`
