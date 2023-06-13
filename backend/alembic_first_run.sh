#!/bin/bash
~/.pyenv/shims/alembic revision --autogenerate -m "Init database"
~/.pyenv/shims/alembic upgrade head