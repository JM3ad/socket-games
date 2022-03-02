FROM python:3.9 as base

WORKDIR /app

RUN useradd -m python && chown python /app
USER python

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=${PATH}:/home/python/.local/bin


COPY *.toml ./

FROM base as dev
RUN poetry install

COPY . .

ENV PYTHONPATH=/app
ENV QUART_APP=tic_tac_toe/app:create_app()
ENTRYPOINT ["poetry", "run", "quart", "run"]
CMD ["--host", "0.0.0.0"]

FROM dev as test
ENTRYPOINT [ "poetry", "run", "pytest" ]
FROM dev as lint
ENTRYPOINT [ "poetry", "run", "black", "--check", "." ]