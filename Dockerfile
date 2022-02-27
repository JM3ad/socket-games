FROM python:3.9 as base

RUN useradd -m python
USER python

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=${PATH}:/home/python/.poetry/bin

WORKDIR /app

COPY *.toml .

FROM base as dev
RUN poetry install

COPY . .

ENV QUART_APP=tic_tac_toe/app:app
ENTRYPOINT ["poetry", "run", "quart", "run"]
CMD ["--host", "0.0.0.0"]

FROM base as prod
RUN poetry install --no-dev

COPY . .

ENTRYPOINT ["poetry", "run", "hypercorn", "tic_tac_toe/app:app"]
CMD ["--bind", "0.0.0.0:5000"]