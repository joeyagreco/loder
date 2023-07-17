@echo off

python scripts\batch\helper\duplicate-test-methods.py
black --config=pyproject.toml .
autoflake --config=pyproject.toml .