@echo off

python scripts\python\duplicate-test-methods.py
black --config=pyproject.toml .
autoflake --config=pyproject.toml .