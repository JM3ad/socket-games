#!/bin/bash

poetry run hypercorn --bind 0.0.0.0:$PORT "tic_tac_toe/app:create_app()"