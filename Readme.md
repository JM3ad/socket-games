# Tic-Tac-Toe

Inspiration taken from Jonesey13.

## Running the project
First time: `poetry install`

To run: `poetry run quart run` or `docker-compose up --build`
The production build:
* `docker build --target prod --tag prod-image .`
* `docker run -itp 5000:5000 --env-file .env prod-image`

Tests: `poetry run pytest`
Format: `poetry run black`

## Intentions

See the project's [Trello Board](https://trello.com/b/ue8k0MhL/socket-games)