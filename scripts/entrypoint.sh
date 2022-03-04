#!/bin/bash

poetry run hypercorn --bind 0.0.0.0:$PORT "socket_games/app:create_app()"