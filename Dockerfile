FROM python:3.9 as base

WORKDIR /app

RUN useradd -m python && chown python /app
USER python

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=${PATH}:/home/python/.local/bin


COPY *.toml ./
ENV PYTHONPATH=/app

FROM base as dev
RUN poetry install

COPY . .

ENTRYPOINT ["poetry", "run", "quart", "run"]
CMD ["--host", "0.0.0.0"]

FROM dev as test
ENTRYPOINT [ "poetry", "run", "pytest" ]
FROM dev as lint
ENTRYPOINT [ "poetry", "run", "black", "--check", "." ]

FROM base as prod
RUN poetry install --no-dev
COPY socket_games ./socket_games
COPY scripts/entrypoint.sh entrypoint.sh
ENV PORT=5000
ENTRYPOINT ["bash", "entrypoint.sh"]
