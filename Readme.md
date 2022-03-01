# Tic-Tac-Toe

Inspiration taken from Jonesey13.

## Running the project
First time: `poetry install`

To run: `poetry run quart run` or `docker-compose up --build`
The production build:
* `docker build --target prod --tag prod-image .`
* `docker run -itp prod-image`

Tests: `poetry run pytest`
Format: `poetry run black`